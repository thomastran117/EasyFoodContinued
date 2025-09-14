from resource.alchemy import User
import bcrypt
from utilities.exception import (
    ConflictException,
    UnauthorizedException,
    NotFoundException,
    BadRequestException,
)
from service.tokenService import (
    create_verification_token,
    get_token_data,
    invalidate_token,
)
from service.emailService import send_verification_email
import datetime
from sqlalchemy.orm import Session
from typing import Optional


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


async def signupUser(db, email: str, password: str):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ConflictException("Email already registered.")

    hashed_pw = hash_password(password)
    token = create_verification_token(email, hashed_pw)

    await send_verification_email(email, token)

    return


def create_user(db, email: str, password: str):

    new_user = User(email=email, password=password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def loginUser(db, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise UnauthorizedException("Invalid credentials.")
    return user


def change_password(db, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise NotFoundException("Email doesn't exist.")

    if verify_password(password, user.password):
        raise BadRequestException("Enter a new password")

    user.password = hash_password(password)

    db.commit()
    db.refresh(user)
    return


from typing import Optional
from sqlalchemy.orm import Session
from resource.alchemy import User


def get_oauth_user(
    db: Session,
    *,
    sub: str,
    email: str,
    name: Optional[str],
    picture: Optional[str],
    provider: str,
) -> User:
    """
    Find or create a user from an OAuth provider (Google or Microsoft).
    Links by provider id first, then by email.
    Updates basic profile fields when they change.
    """

    provider_id_field = {
        "google": "google_id",
        "microsoft": "microsoft_id",
    }.get(provider)

    if not provider_id_field:
        raise ValueError(f"Unsupported provider: {provider}")

    user = db.query(User).filter(getattr(User, provider_id_field) == sub).first()
    if user:
        changed = False
        if name and user.name != name:
            user.name = name
            changed = True
        if picture and user.profileUrl != picture:
            user.profileUrl = picture
            changed = True
        if changed:
            db.commit()
            db.refresh(user)
        return user

    user = db.query(User).filter(User.email == email).first()
    if user:
        setattr(user, provider_id_field, sub)
        user.provider = provider
        if name and not user.name:
            user.name = name
        if picture and not user.profileUrl:
            user.profileUrl = picture
        db.commit()
        db.refresh(user)
        return user

    user = User(
        email=email,
        password=None,
        role="user",
        provider=provider,
        **{provider_id_field: sub},
        name=name,
        profileUrl=picture,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
