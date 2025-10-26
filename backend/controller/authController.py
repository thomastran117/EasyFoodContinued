from fastapi import Request, Response
from fastapi.responses import JSONResponse

from config.envConfig import settings
from dtos.authDtos import (
    ChangePasswordDto,
    ForgotPasswordDto,
    GoogleAuthRequest,
    LoginRequestDto,
    MicrosoftAuthRequest,
    SignupRequestDto,
)
from service.authService import (
    changePassword,
    exchangeTokens,
    forgotPassword,
    google_login,
    loginUser,
    logoutTokens,
    microsoft_login,
    signupUser,
    verifyUser,
)
from utilities.errorRaiser import (
    ServiceUnavaliableException,
    UnauthorizedException,
    raise_error,
)
from utilities.logger import logger


async def login(request: LoginRequestDto):
    try:
        access, refresh, user = await loginUser(
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

        return set_refresh_cookie(response, refresh)

    except Exception as e:
        raise_error(e)


async def signup(request: SignupRequestDto):
    try:
        await signupUser(request.email, request.password, request.role, request.captcha)
        return {"message": "Verification sent. Check your email"}
    except Exception as e:
        raise_error(e)


async def verify_email(token: str):
    try:
        if not settings.email_enabled:
            logger.warn("Email service is not avaliable. Please correct")
            raise ServiceUnavaliableException("Email verification  is not avaliable")
        user = await verifyUser(token)
        return {"message": "Signup successful"}
    except Exception as e:
        raise_error(e)


async def renew(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException("Missing  refresh token cookie")
        access, refresh, email = await exchangeTokens(refresh_token)
        response = JSONResponse(
            content={
                "token": access,
                "email": email,
                "username": "hello",
                "role": "me",
                "avatar": "hi",
            }
        )

        return set_refresh_cookie(response, refresh)

    except Exception as e:
        raise_error(e)


async def logout(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException("No refresh token cookie found")

        await logoutTokens(refresh_token)

        response = JSONResponse({"message": "Logged out successfully"})
        response.delete_cookie(
            key="refresh_token",
            httponly=True,
            secure=False,
            samesite="lax",
        )
        return response

    except Exception as e:
        raise_error(e)


async def forgot_password(request: ForgotPasswordDto):
    try:
        if not settings.email_enabled:
            logger.warn("Email service is not avaliable. Please correct")
            raise ServiceUnavaliableException(
                "Forgot password is not avaliable right now"
            )
        await forgotPassword(request.email)
        return {"message": "If your email exists, a reset link was sent."}
    except Exception as e:
        raise_error(e)


async def change_password(token: str, request: ChangePasswordDto):
    try:
        if not settings.email_enabled:
            logger.warn("Email service is not avaliable. Please correct")
            raise ServiceUnavaliableException(
                "Change password is not avaliable right now"
            )
        user = await changePassword(request.password, token)
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise_error(e)


async def google(auth_req: GoogleAuthRequest):
    try:

        access, refresh, user = await google_login(auth_req.id_token, False)

        response = JSONResponse(
            content={
                "message": "Login successful",
                "token": access,
                "username": user.username if user.username else user.email,
                "avatar": user.avatar,
                "role": user.role,
            }
        )

        return set_refresh_cookie(response, refresh)

    except Exception as e:
        raise_error(e)


async def microsoft(auth_req: MicrosoftAuthRequest):
    try:
        access, refresh, user = await microsoft_login(auth_req.id_token, False)

        response = JSONResponse(
            content={
                "message": "Login successful",
                "token": access,
                "username": user.username if user.username else user.email,
                "avatar": user.avatar,
                "role": user.role,
            }
        )

        return set_refresh_cookie(response, refresh)

    except Exception as e:
        raise_error(e)


def set_refresh_cookie(response: Response, refresh_token: str):
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
