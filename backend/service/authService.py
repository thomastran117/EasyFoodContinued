import bcrypt
import httpx
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt as jose_jwt

from config.envConfig import settings
from resources.database_client import get_db
from schema.template import User
from service.emailService import send_forgot_password_email, send_verification_email
from service.tokenService import (
    create_verification_token,
    generate_tokens,
    invalidate_refresh_token,
    rotate_refresh_token,
    verify_verification_token,
)
from service.webService import google_verify_captcha
from utilities.errorRaiser import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    ServiceUnavaliableException,
    UnauthorizedException,
)
from utilities.logger import logger


async def loginUser(email: str, password: str, captcha: str, remember: bool = False):
    if settings.recaptcha_enabled:
        is_valid_captcha = await google_verify_captcha(captcha)
        if not is_valid_captcha:
            raise UnauthorizedException("Captcha verification failed.")
    else:
        logger.warn(
            "Bot detection can't be served due to unavaliable captcha configuration"
        )

    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise UnauthorizedException("Invalid email or password.")

    access, refresh = generate_tokens(user.id, user.email, "user", remember)
    return access, refresh, user


async def signupUser(email: str, password: str, role: str, captcha: str):
    if settings.recaptcha_enabled:
        is_valid_captcha = await google_verify_captcha(captcha)
        if not is_valid_captcha:
            raise UnauthorizedException("Captcha verification failed.")
    else:
        logger.warn("Bot detection can't be served due to captcha misconfiguration")

    with get_db() as db:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ConflictException(f"The email '{email}' is already registered.")

        hashed_pw = hash_password(password)

        if not settings.email_enabled:
            logger.warn(
                "Verifying users can't be served due to email misconfiguration. Defaulting."
            )
            new_user = User(email=email, password=hashed_pw)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

    if settings.email_enabled:
        token = create_verification_token(email, hashed_pw)
        await send_verification_email(email, token)

    return True


async def verifyUser(token: str):
    if not settings.email_enabled:
        logger.warn("Verifying users can't be served due to email misconfiguration.")
        raise ServiceUnavaliableException("Email verification is not avaliable")

    with get_db() as db:
        data = verify_verification_token(token)
        if not data:
            raise BadRequestException("Invalid token")
        new_user = User(email=data["email"], password=data["password"])

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


async def microsoft_login(id_token: str, remember: bool = False):
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://login.microsoftonline.com/common/discovery/v2.0/keys"
        )
        resp.raise_for_status()
        jwks = resp.json()

    header = jose_jwt.get_unverified_header(id_token)
    kid = header.get("kid")

    key = next((k for k in jwks["keys"] if k["kid"] == kid), None)
    if not key:
        raise BadRequestException("Unable to find matching JWKS key")

    decoded_ms = jose_jwt.decode(
        id_token,
        key,
        algorithms=["RS256"],
        audience=settings.ms_client_id,
        options={"verify_iss": False},
    )

    email = decoded_ms.get("preferred_username") or decoded_ms.get("email")
    user_id = decoded_ms.get("sub")
    name = decoded_ms.get("name")
    picture = decoded_ms.get("picture")

    if not email:
        raise UnauthorizedException("No email claim in Microsoft token")

    with get_db() as db:
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

    access, refresh = generate_tokens(user.id, user.email, user.role, remember)
    return access, refresh, user


async def google_login(token: str, remember: bool = False):
    idinfo = id_token.verify_oauth2_token(
        token, requests.Request(), settings.google_client_id
    )

    if idinfo["iss"] not in [
        "accounts.google.com",
        "https://accounts.google.com",
    ]:
        raise UnauthorizedException("Invalid issuer.")

    email = idinfo.get("email")
    name = idinfo.get("name")
    picture = idinfo.get("picture")
    user_id = idinfo.get("sub")

    with get_db() as db:
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

    access, refresh = generate_tokens(user.id, user.email, user.role, remember)
    return access, refresh, user


async def forgotPassword(email: str):
    if not settings.email_enabled:
        logger.warn("Forgot password can't be served due to email misconfiguration.")
        raise ServiceUnavaliableException("Forgot password servce is unavaliable")

    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return

        if user.provider in ["google", "microsoft"]:
            return

    token = create_verification_token(email, "empty")
    await send_forgot_password_email(email, token)

    return


async def changePassword(password: str, token: str):
    if not settings.email_enabled:
        logger.warn("Change password can't be served due to email misconfiguration.")
        raise ServiceUnavaliableException("Change password service is unavaliable")

    data = verify_verification_token(token)
    if not data:
        raise BadRequestException("Invalid or expired token")

    with get_db() as db:

        email = data["email"]

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise NotFoundException("User not found")

        hashed_pw = hash_password(password)
        user.password = hashed_pw

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


async def exchangeTokens(token: str):
    access, refresh, email = rotate_refresh_token(token)
    return access, refresh, email


async def logoutTokens(token: str):
    invalidate_refresh_token(token)
    return {"message": "Logged out successfully"}


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
