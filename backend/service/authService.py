import bcrypt
import httpx
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt as jose_jwt

from config.environmentConfig import settings
from resources.database_client import get_db
from schema.psql_template import User
from service.tokenService import TokenService
from service.emailService import EmailService
from service.oauthService import OAuthService
from service.webService import WebService
from utilities.errorRaiser import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    ServiceUnavaliableException,
    UnauthorizedException,
)
from utilities.logger import logger


class AuthService:
    def __init__(
        self,
        token_service: TokenService,
        email_service: EmailService,
        oauth_service: OAuthService,
        web_service: WebService,
        db_factory=get_db,
    ):
        """
        token_service: instance of TokenService
        """
        self.token_service = token_service
        self.email_service = email_service
        self.oauth_service = oauth_service
        self.web_service = web_service
        self.db_factory = db_factory

    async def login_user(
        self, email: str, password: str, captcha: str, remember: bool = False
    ):
        if settings.recaptcha_enabled:
            is_valid_captcha = await self.web_service.verifyGoogleCaptcha(captcha)
            if not is_valid_captcha:
                raise UnauthorizedException("Captcha verification failed.")
        else:
            logger.warn(
                "Bot detection can't be served due to unavailable captcha configuration"
            )

        with self.db_factory() as db:
            user = db.query(User).filter(User.email == email).first()

        if not user or not self.verify_password(password, user.password):
            raise UnauthorizedException("Invalid email or password.")

        access, refresh = self.token_service.generate_tokens(
            user.id, user.email, "user", remember
        )
        return access, refresh, user

    async def signup_user(self, email: str, password: str, role: str, captcha: str):
        if settings.recaptcha_enabled:
            is_valid_captcha = await self.web_service.verifyGoogleCaptcha(captcha)
            if not is_valid_captcha:
                raise UnauthorizedException("Captcha verification failed.")
        else:
            logger.warn("Bot detection can't be served due to captcha misconfiguration")

        with self.db_factory() as db:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                raise ConflictException(f"The email '{email}' is already registered.")

            hashed_pw = self.hash_password(password)

            if not settings.email_enabled:
                logger.warn(
                    "Verifying users can't be served due to email misconfiguration. Defaulting."
                )
                new_user = User(email=email, password=hashed_pw)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return True

        if settings.email_enabled:
            token = self.token_service.create_verification_token(email, hashed_pw)
            await self.email_service.send_verification_email(email, token)

        return True

    async def verify_user(self, token: str):
        if not settings.email_enabled:
            logger.warn(
                "Verifying users can't be served due to email misconfiguration."
            )
            raise ServiceUnavaliableException("Email verification is not available")

        with self.db_factory() as db:
            data = self.token_service.verify_verification_token(token)
            if not data:
                raise BadRequestException("Invalid token")

            new_user = User(email=data["email"], password=data["password"])
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

    async def microsoft_login(self, token: str, remember: bool = False):
        email, user_id, name, picture = await self.oauth_service.verifyMicrosoftToken(
            token
        )

        if not email:
            raise UnauthorizedException("No email claim in Microsoft token")

        with self.db_factory() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    provider="microsoft",
                    microsoft_id=user_id,
                    name=name,
                    avatar=picture,
                )
                db.add(user)
            else:
                if not user.microsoft_id:
                    user.microsoft_id = user_id
                if not user.provider or user.provider == "local":
                    user.provider = "microsoft"

            db.commit()
            db.refresh(user)

        access, refresh = self.token_service.generate_tokens(
            user.id, user.email, user.role, remember
        )
        return access, refresh, user

    async def google_login(self, token: str, remember: bool = False):
        email, name, picture, user_id = await self.oauth_service.verifyGoogleToken(
            token
        )

        with self.db_factory() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                user = User(
                    email=email,
                    provider="google",
                    microsoft_id=user_id,
                    name=name,
                    avatar=picture,
                )
                db.add(user)
                db.commit()
                db.refresh(user)

        access, refresh = self.token_service.generate_tokens(
            user.id, user.email, user.role, remember
        )
        return access, refresh, user

    async def forgot_password(self, email: str):
        if not settings.email_enabled:
            logger.warn(
                "Forgot password can't be served due to email misconfiguration."
            )
            raise ServiceUnavaliableException("Forgot password service is unavailable")

        with self.db_factory() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return
            if user.provider in ["google", "microsoft"]:
                return

        token = self.token_service.create_verification_token(email, "empty")
        await self.email_service.send_forgot_password_email(email, token)
        return

    async def change_password(self, password: str, token: str):
        if not settings.email_enabled:
            logger.warn(
                "Change password can't be served due to email misconfiguration."
            )
            raise ServiceUnavaliableException("Change password service is unavailable")

        data = self.token_service.verify_verification_token(token)
        if not data:
            raise BadRequestException("Invalid or expired token")

        with self.db_factory() as db:
            email = data["email"]
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise NotFoundException("User not found")

            hashed_pw = self.hash_password(password)
            user.password = hashed_pw
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    async def exchange_tokens(self, token: str):
        access, refresh, email = self.token_service.rotate_refresh_token(token)
        return access, refresh, email

    async def logout_tokens(self, token: str):
        self.token_service.invalidate_refresh_token(token)
        return {"message": "Logged out successfully"}

    def hash_password(self, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
