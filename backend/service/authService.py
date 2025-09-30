from resources.alchemy import User, get_db
import bcrypt
from utilities.errorRaiser import (
    ConflictException,
    UnauthorizedException,
    BadRequestException,
)
from service.tokenService import (
    generate_tokens,
    rotate_refresh_token,
    create_verification_token,
    verify_verification_token,
)
from service.emailService import send_verification_email


async def loginUser(email: str, password: str):
    with get_db() as db:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            raise UnauthorizedException("Invalid credentials.")
        access, refresh = generate_tokens(user.id, user.email, "user")
        return access, refresh, user


async def signupUser(email: str, password: str):
    with get_db() as db:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ConflictException("Email already registered.")

        hashed_pw = hash_password(password)
        token = create_verification_token(email, hashed_pw)

        await send_verification_email(email, token)

        return True


async def verifyUser(token: str):
    with get_db() as db:
        data = verify_verification_token(token)
        if not data:
            raise BadRequestException("Invalid token")
        new_user = User(email=data["email"], password=data["password"])

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def createUser(email: str, password: str):
    with get_db() as db:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ConflictException("Email already registered.")
        hashed_pw = hash_password(password)
        new_user = User(email=email, password=hashed_pw)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


async def exchangeTokens(token: str):
    access, refresh, email = await rotate_refresh_token(token)
    return access, refresh, email


async def logoutTokens(token: str):
    pass


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )
