from fastapi import Request
from fastapi.responses import JSONResponse
from service.authService import (
    loginUser,
    signupUser,
    createUser,
    verifyUser,
    exchangeTokens,
    logoutTokens,
)

from dtos.authDtos import AuthRequestDto
from utilities.errorRaiser import (
    raise_error,
    ServiceUnavaliableException,
    UnauthorizedException,
    NotImplementedException,
)
from config.envConfig import settings
from utilities.logger import logger


async def login(request: AuthRequestDto):
    try:
        access, refresh, user = await loginUser(request.email, request.password)

        response = JSONResponse(
            content={
                "token": access,
                "email": user.email,
            }
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
    except Exception as e:
        raise_error(e)


async def signup(request: AuthRequestDto):
    try:
        if not settings.email_enabled:
            logger.warn(
                "Email service is not avaliable. Proceeding with signing up the user w/o verification"
            )
            await createUser(request.email, request.password)
            return {"message": "Signup completed without verification. Please login"}
        else:
            await signupUser(request.email, request.password)
            return {"message": "Verification sent. Check your email"}
    except Exception as e:
        raise_error(e)


async def verify_email(token: str):
    try:
        if not settings.email_enabled:
            logger.warn("Email service is not avaliable. Please correct")
            raise ServiceUnavaliableException("Verification route is not avaliable")
        user = await verifyUser(token)
        return {"message": "Signup successful"}
    except Exception as e:
        raise_error(e)


async def renew(request: Request):
    try:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException("Missing refresh token cookie")
        access, refresh, email = await exchangeTokens(refresh_token)
        response = JSONResponse(
            content={
                "token": access,
                "email": email,
            }
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response
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
            secure=True,
            samesite="Lax",
        )
        return response

    except Exception as e:
        raise_error(e)


async def google():
    try:
        raise NotImplementedException("Google OAuth is not implemented yet")
    except Exception as e:
        raise_error(e)


async def microsoft():
    try:
        raise NotImplementedException("Microsoft OAuth is not implemented yet")
    except Exception as e:
        raise_error(e)
