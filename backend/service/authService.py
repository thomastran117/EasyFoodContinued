import bcrypt

from resources.database_client import get_db
from schema.psql_template import User
from service.emailService import EmailService
from service.oauthService import OAuthService
from service.tokenService import TokenService
from service.webService import WebService
from utilities.errorRaiser import (
    AppHttpException,
    BadRequestException,
    ConflictException,
    InternalErrorException,
    NotFoundException,
    ServiceUnavailableException,
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
        self.token_service = token_service
        self.email_service = email_service
        self.oauth_service = oauth_service
        self.web_service = web_service
        self.db_factory = db_factory
        self.DUMMY_HASH = "$2b$10$CwTycUXWue0Thq9StjUM0uJ8T8YtAUD3bFIxVYbcEdb87qfEzS1mS"

    async def localAuthenticate(
        self, email: str, password: str, captcha: str, remember: bool = False
    ):
        try:
            if self.web_service.isRecaptchaAvaliable():
                is_valid_captcha = await self.web_service.verifyGoogleCaptcha(captcha)
                if not is_valid_captcha:
                    raise UnauthorizedException("Invalid captcha")
            else:
                logger.warn(
                    f"[AuthService] localAuthenticate: WebService is misconfigured - skipping recaptcha"
                )

            with self.db_factory() as db:
                user = db.query(User).filter(User.email == email).first()
        
            hash_to_check = user.password if user and user.password else self.DUMMY_HASH
            password_ok = self.verifyPassword(password, hash_to_check)

            if not user or not password_ok:
                raise UnauthorizedException("Invalid email or password.")

            access, refresh = self.token_service.generateTokens(
                user.id, user.email, "user", remember
            )
            return access, refresh, user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] localAuthenticate failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def signupUser(self, email: str, password: str, role: str, captcha: str):
        try:
            if self.web_service.isRecaptchaAvaliable():
                is_valid_captcha = await self.web_service.verifyGoogleCaptcha(captcha)
                if not is_valid_captcha:
                    raise UnauthorizedException("Invalid captcha")
            else:
                logger.warn(
                    f"[AuthService] localAuthenticate: WebService is misconfigured - skipping recaptcha"
                )

            with self.db_factory() as db:
                existing_user = db.query(User).filter(User.email == email).first()
                if existing_user:
                    raise ConflictException(
                        f"The email '{email}' is already registered."
                    )

                hashed_pw = self.hashPassword(password)

                if not self.email_service.isEmailAvaliable():
                    logger.warn(
                        "[AuthService] signupUser: Email service is misconfigured - skipping verification"
                    )
                    new_user = User(email=email, password=hashed_pw)
                    db.add(new_user)
                    db.commit()
                    db.refresh(new_user)
                    return True

            if self.email_service.isEmailAvaliable():
                token = self.token_service.createVerificationToken(email, hashed_pw)
                await self.email_service.send_verification_email(email, token)

            return True
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] signupUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def verifyUser(self, token: str):
        try:
            if not self.email_service.isEmailAvaliable():
                logger.warn("[AuthService] Email service is misconfigured - exiting")
                raise ServiceUnavailableException(
                    "The server is not ready to handle the request"
                )

            with self.db_factory() as db:
                data = self.token_service.verifyVerificationToken(token)
                if not data:
                    raise BadRequestException("Invalid token")

                new_user = User(email=data["email"], password=data["password"])
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return new_user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] verifyUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def microsoftOAuth(self, token: str, remember: bool = False):
        try:
            email, user_id, name, picture = (
                await self.oauth_service.verifyMicrosoftToken(token)
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
                    db.commit()
                    db.refresh(user)

            access, refresh = self.token_service.generateTokens(
                user.id, user.email, user.role, remember
            )
            return access, refresh, user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] microsoftOAuth failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def googleOAuth(self, token: str, remember: bool = False):
        try:
            email, name, picture, user_id = await self.oauth_service.verifyGoogleToken(
                token
            )
            with self.db_factory() as db:
                user = db.query(User).filter(User.email == email).first()
                if not user:
                    user = User(
                        email=email,
                        provider="google",
                        google_id=user_id,
                        name=name,
                        avatar=picture,
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)

            access, refresh = self.token_service.generateTokens(
                user.id, user.email, user.role, remember
            )
            return access, refresh, user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] googleOAuth failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def forgotPassword(self, email: str):
        try:
            if not self.email_service.isEmailAvaliable():
                logger.warn(
                    "[AuthService] forgotPassword: WebService has invalid configuration - exiting"
                )
                raise ServiceUnavailableException(
                    "The server is not ready to handle the request"
                )

            with self.db_factory() as db:
                user = db.query(User).filter(User.email == email).first()
                if not user:
                    return
                if user.provider in ["google", "microsoft"]:
                    return

            token = self.token_service.createVerificationToken(email, "empty")
            await self.email_service.send_forgot_password_email(email, token)
            return
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] forgotPassword failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def changePassword(self, password: str, token: str):
        try:
            if not self.email_service.isEmailAvaliable():
                logger.warn(
                    "[AuthService] changePassword: WebService has invalid configuration - exiting"
                )
                raise ServiceUnavailableException(
                    "The server is not ready to handle the request"
                )

            data = self.token_service.verifyVerificationToken(token)
            if not data:
                raise BadRequestException("Invalid or expired token")

            with self.db_factory() as db:
                email = data["email"]
                user = db.query(User).filter(User.email == email).first()
                if not user:
                    raise NotFoundException("User not found")

                hashed_pw = self.hashPassword(password)
                user.password = hashed_pw
                db.add(user)
                db.commit()
                db.refresh(user)
                return
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] changePassword failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def exchangeTokens(self, token: str):
        try:
            access, refresh, email = self.token_service.rotateTokens(token)
            return access, refresh, email
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] exchangeTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def logoutTokens(self, token: str):
        try:
            self.token_service.logoutToken(token)
            return {"message": "Logged out successfully"}
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] logoutTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def hashPassword(self, plain_password: str) -> str:
        try:
            return bcrypt.hashpw(
                plain_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] hashPassword failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def verifyPassword(self, plain_password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] verifyPassword failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
