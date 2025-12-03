import bcrypt

from repository.userRepository import UserRepository
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
        user_repository: UserRepository,
        token_service: TokenService,
        email_service: EmailService,
        oauth_service: OAuthService,
        web_service: WebService,
    ):
        self.user_repository = user_repository
        self.token_service = token_service
        self.email_service = email_service
        self.oauth_service = oauth_service
        self.web_service = web_service
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

            user = await self.user_repository.getByEmail(email)

            hash_to_check = user.password if user and user.password else self.DUMMY_HASH
            password_ok = self.verifyPassword(password, hash_to_check)

            if not user or not password_ok:
                raise UnauthorizedException("Invalid email or password.")

            access, refresh = await self.token_service.generateTokens(
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

            existing_user = await self.user_repository.getByEmail(email)
            if existing_user:
                raise ConflictException(f"The email '{email}' is already registered.")

            hashed_pw = self.hashPassword(password)

            if not self.email_service.isEmailAvaliable():
                logger.warn(
                    "[AuthService] signupUser: Email service is misconfigured - skipping verification"
                )
                await self.user_repository.create(email, "local", role, password)
            else:
                token = await self.token_service.createVerificationToken(
                    email, hashed_pw
                )
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

            data = self.token_service.verifyVerificationToken(token)
            if not data:
                raise BadRequestException("Invalid token")

            new_user = await self.user_repository.create(
                data["email"], "local", data["role"], data["password"]
            )

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

            user = await self.user_repository.getByEmail(
                email
            ) or await self.user_repository.getByMicrosoftId(user_id)

            if not user:
                user = await self.user_repository.create(
                    email=email,
                    provider="microsoft",
                    role="undefined",
                    microsoft_id=user_id,
                )

            access, refresh = await self.token_service.generateTokens(
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
            user = await self.user_repository.getByEmail(
                email
            ) or await self.user_repository.getByGoogleId(user_id)

            if not user:
                user = await self.user_repository.create(
                    email=email, provider="google", role="undefined", google_id=user_id
                )

            access, refresh = await self.token_service.generateTokens(
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

            user = await self.user_repository.getByEmail(email)
            if not user:
                return
            if user.provider in ["google", "microsoft"]:
                return

            token = await self.token_service.createVerificationToken(email, "empty")
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

            data = await self.token_service.verifyVerificationToken(token)
            if not data:
                raise BadRequestException("Invalid or expired token")

            user = await self.user_repository.getByEmail(data["email"])
            if not user:
                raise NotFoundException("User not found")

            hashed_password = self.hashPassword(password)

            updated_user = await self.user_repository.update(
                user.id, {"password": hashed_password}
            )

            return updated_user

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] changePassword failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def exchangeTokens(self, token: str):
        try:
            access, refresh, email = await self.token_service.rotateTokens(token)
            return access, refresh, email
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[AuthService] exchangeTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def logoutTokens(self, token: str):
        try:
            await self.token_service.logoutToken(token)
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
