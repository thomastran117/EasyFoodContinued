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
from utilities.errorRaiser import AppHttpException, UnauthorizedException, raise_error
from utilities.logger import logger


class AuthController:
    def __init__(self, authservice: AuthService):
        """
        auth_service: instance of AuthService (which uses TokenService internally)
        """
        self.auth_service = authservice
        self.request: Request | None = None

    async def login(self, request: LoginRequestDto):
        try:
            access, refresh, user = await self.auth_service.localAuthenticate(
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
            return self.setRefreshCookie(response, refresh)
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] login failed: {e}")
            raise_error(e)

    async def signup(self, request: SignupRequestDto):
        try:
            await self.auth_service.signupUser(
                request.email, request.password, request.role, request.captcha
            )
            return {"message": "Verification sent. Check your email"}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] signup failed: {e}")
            raise_error(e)

    async def verifyUser(self, token: str):
        try:
            await self.auth_service.verifyUser(token)
            return {"message": "Signup successful"}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] verifyUser failed: {e}")
            raise_error(e)

    async def renew(self):
        try:
            refresh_token = self.request.cookies.get("refresh_token")
            if not refresh_token:
                raise UnauthorizedException("Missing refresh token cookie")

            access, refresh, email = await self.auth_service.exchangeTokens(
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
            return self.setRefreshCookie(response, refresh)
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] renew failed: {e}")
            raise_error(e)

    async def logout(self):
        try:
            refresh_token = self.request.cookies.get("refresh_token")
            if not refresh_token:
                raise UnauthorizedException("No refresh token cookie found")

            await self.auth_service.logoutTokens(refresh_token)
            response = JSONResponse({"message": "Logged out successfully"})
            response.delete_cookie(
                key="refresh_token",
                httponly=True,
                secure=not getattr(settings, "debug", False),
                samesite="lax",
            )
            return response
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] logout failed: {e}")
            raise_error(e)

    async def forgotPassword(self, request: ForgotPasswordDto):
        try:
            await self.auth_service.forgotPassword(request.email)
            return {"message": "If this email exists, a password reset link was sent."}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] forgotPassword failed: {e}")
            raise_error(e)

    async def changePassword(self, token: str, request: ChangePasswordDto):
        try:
            await self.auth_service.changePassword(request.password, token)
            return {"message": "Password changed successfully"}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] changePassword failed: {e}")
            raise_error(e)

    async def googleOAuth(self, auth_req: GoogleAuthRequest):
        try:
            access, refresh, user = await self.auth_service.googleOAuth(
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
            return self.setRefreshCookie(response, refresh)
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] googleOAuth failed: {e}")
            raise_error(e)

    async def microsoftOAuth(self, auth_req: MicrosoftAuthRequest):
        try:
            access, refresh, user = await self.auth_service.microsoftOAuth(
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
            return self.setRefreshCookie(response, refresh)

        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] microsoftOAuth failed: {e}")
            raise_error(e)

    def setRefreshCookie(self, response: Response, refresh_token: str):
        try:
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
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[AuthController] setRefreshCookie failed: {e}")
            raise_error(e)
