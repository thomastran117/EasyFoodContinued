from fastapi import Request, Response
from fastapi.responses import JSONResponse

from config.environmentConfig import settings
from dtos.authDtos import (
    ChangePasswordDto,
    ForgotPasswordDto,
    GoogleAuthRequest,
    LoginRequestDto,
    MicrosoftAuthRequest,
    SignupRequestDto,
)
from service.authService import AuthService
from utilities.errorRaiser import (
    ServiceUnavailableException,
    UnauthorizedException,
    raise_error,
)
from utilities.logger import logger


class AuthController:
    def __init__(self, auth_service: AuthService):
        """
        auth_service: instance of AuthService (which uses TokenService internally)
        """
        self.auth_service = auth_service
        self.request: Request | None = None

    async def login(self, request: LoginRequestDto):
        try:
            access, refresh, user = await self.auth_service.login_user(
                request.email, request.password, request.captcha, request.remember
            )

            response = JSONResponse(
                content={
                    "message": "Login successful",
                    "token": access,
                    "username": user.username if user.username else user.email,
                    "avatar": user.avatar,
                    "role": user.role,
                }
            )
            return self._set_refresh_cookie(response, refresh)

        except Exception as e:
            raise_error(e)

    async def signup(self, request: SignupRequestDto):
        try:
            await self.auth_service.signup_user(
                request.email, request.password, request.role, request.captcha
            )
            return {"message": "Verification sent. Check your email"}
        except Exception as e:
            raise_error(e)

    async def verify_email(self, token: str):
        try:
            if not settings.email_enabled:
                logger.warn("Email service is not available. Please correct")
                raise ServiceUnavailableException("Email verification is not available")
            await self.auth_service.verify_user(token)
            return {"message": "Signup successful"}
        except Exception as e:
            raise_error(e)

    async def renew(self):
        try:
            refresh_token = self.request.cookies.get("refresh_token")
            if not refresh_token:
                raise UnauthorizedException("Missing refresh token cookie")

            access, refresh, email = await self.auth_service.exchange_tokens(
                refresh_token
            )
            response = JSONResponse(
                content={
                    "token": access,
                    "email": email,
                    "username": "hello",
                    "role": "me",
                    "avatar": "hi",
                }
            )
            return self._set_refresh_cookie(response, refresh)

        except Exception as e:
            raise_error(e)

    async def logout(self):
        try:
            refresh_token = self.request.cookies.get("refresh_token")
            if not refresh_token:
                raise UnauthorizedException("No refresh token cookie found")

            await self.auth_service.logout_tokens(refresh_token)
            response = JSONResponse({"message": "Logged out successfully"})
            response.delete_cookie(
                key="refresh_token",
                httponly=True,
                secure=not getattr(settings, "debug", False),
                samesite="lax",
            )
            return response
        except Exception as e:
            raise_error(e)

    async def forgot_password(self, request: ForgotPasswordDto):
        try:
            if not settings.email_enabled:
                logger.warn("Email service is not available. Please correct")
                raise ServiceUnavailableException("Forgot password is not available")

            await self.auth_service.forgot_password(request.email)
            return {"message": "If your email exists, a reset link was sent."}

        except Exception as e:
            raise_error(e)

    async def change_password(self, token: str, request: ChangePasswordDto):
        try:
            if not settings.email_enabled:
                logger.warn("Email service is not available. Please correct")
                raise ServiceUnavailableException("Change password is not available")

            await self.auth_service.change_password(request.password, token)
            return {"message": "Password changed successfully"}
        except Exception as e:
            raise_error(e)

    async def google(self, auth_req: GoogleAuthRequest):
        try:
            access, refresh, user = await self.auth_service.google_login(
                auth_req.id_token, False
            )

            response = JSONResponse(
                content={
                    "message": "Login successful",
                    "token": access,
                    "username": user.username if user.username else user.email,
                    "avatar": user.avatar,
                    "role": user.role,
                }
            )
            return self._set_refresh_cookie(response, refresh)

        except Exception as e:
            raise_error(e)

    async def microsoft(self, auth_req: MicrosoftAuthRequest):
        try:
            access, refresh, user = await self.auth_service.microsoft_login(
                auth_req.id_token, False
            )

            response = JSONResponse(
                content={
                    "message": "Login successful",
                    "token": access,
                    "username": user.username if user.username else user.email,
                    "avatar": user.avatar,
                    "role": user.role,
                }
            )
            return self._set_refresh_cookie(response, refresh)

        except Exception as e:
            raise_error(e)

    def _set_refresh_cookie(self, response: Response, refresh_token: str):
        secure_flag = not getattr(settings, "debug", False)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=secure_flag,
            samesite="None",
            path="/",
            max_age=7 * 24 * 60 * 60,
        )
        return response
