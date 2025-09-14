from fastapi import HTTPException, Request
from service.authService import (
    loginUser,
    signupUser,
    change_password,
    create_user,
    get_oauth_user,
)
from service.tokenService import create_token, get_token_data, invalidate_token
from dtos.authDtos import AuthRequestDto, AuthResponseDto
from utilities.errorRaiser import raise_error
from utilities.exception import BadRequestException
from resources.alchemy import SessionLocal
from config.envConfig import settings
from starlette.responses import RedirectResponse
from middleware.oauth import oauth


async def login(request: AuthRequestDto):
    db = SessionLocal()
    try:
        user = loginUser(db, request.email, request.password)

        user_data = {"id": user.id, "email": user.email, "role": "user"}

        token = create_token(user_data)
        return {"token": token, "email": user.email}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def signup(request: AuthRequestDto):
    db = SessionLocal()
    try:
        await signupUser(db, request.email, request.password)
        return {"message": "Check your email"}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def verify_email(token: str):
    db = SessionLocal()
    try:
        data = get_token_data(token)
        if not data:
            raise BadRequestException("Invalid token")
        new_user = create_user(db, data["email"], data["password"])
        return {"message": "Signup successful", "user_id": new_user.id}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()


async def renew_token(request):
    pass


async def google_login(request: Request):
    redirect_uri = settings.google_redirect_uri
    return await oauth.google.authorize_redirect(request, redirect_uri)


async def google_callback(request: Request):
    db = SessionLocal()
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = await oauth.google.parse_id_token(request, token)
        if not userinfo:
            raise HTTPException(
                status_code=400, detail="Failed to retrieve Google profile."
            )

        sub = userinfo.get("sub")
        email = userinfo.get("email")
        name = userinfo.get("name")
        picture = userinfo.get("picture")

        if not sub or not email:
            raise HTTPException(status_code=400, detail="Google profile incomplete.")

        user = get_oauth_user(
            db,
            sub=sub,
            email=email,
            name=name,
            picture=picture,
            provider="google",
        )

        jwt = create_token({"id": user.id, "email": user.email, "role": user.role})
        return {
            "token": jwt,
            "email": user.email,
            "name": user.name,
            "avatar": user.profileUrl,
        }
    finally:
        db.close()


async def microsoft_start(request: Request):
    redirect_uri = settings.ms_redirect_uri
    return await oauth.microsoft.authorize_redirect(request, redirect_uri)


async def microsoft_callback(request: Request):
    db = SessionLocal()
    try:
        token = await oauth.microsoft.authorize_access_token(request)
        userinfo = await oauth.microsoft.parse_id_token(request, token)
        if not userinfo:
            raise HTTPException(
                status_code=400, detail="Failed to retrieve Microsoft profile."
            )

        sub = userinfo.get("sub")
        email = userinfo.get("email") or userinfo.get("preferred_username")
        name = userinfo.get("name")
        picture = userinfo.get("picture")

        if not sub or not email:
            raise HTTPException(status_code=400, detail="Microsoft profile incomplete.")

        user = get_oauth_user(
            db,
            sub=sub,
            email=email,
            name=name,
            picture=picture,
            provider="microsoft",
        )

        jwt = create_token({"id": user.id, "email": user.email, "role": user.role})
        return {
            "token": jwt,
            "email": user.email,
            "name": user.name,
            "avatar": user.profileUrl,
        }
    finally:
        db.close()
