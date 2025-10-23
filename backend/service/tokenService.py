import json
import secrets
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from resources.redis_client import redis_client
from config.envConfig import settings
from utilities.errorRaiser import UnauthorizedException, ForbiddenException


JWT_SECRET_ACCESS = settings.jwt_secret_access
JWT_SECRET_REFRESH = settings.jwt_secret_refresh + "_refresh"
JWT_SECRET_VERIFY = settings.jwt_secret_verify + "_verify"

ALGORITHM = settings.algorithm

ACCESS_EXPIRE_MINUTES = 15
REFRESH_EXPIRE_DAYS_SHORT = 1
REFRESH_EXPIRE_DAYS_LONG = 7
VERIFY_EXPIRE_MINUTES = 60


require_auth_token = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(require_auth_token)) -> dict:
    payload = decode_access_token(token)
    required = ("id", "email", "role")
    if not all(payload.get(f) for f in required):
        raise UnauthorizedException("Invalid token payload")
    return {f: payload[f] for f in required}


def require_role(*roles: str):
    def role_dependency(user: dict = Depends(get_current_user)):
        role = user.get("role")
        if role not in roles:
            raise ForbiddenException(f"Insufficient privileges: requires {roles}, found '{role}'")
        
        return user

    return role_dependency

def _refresh_key(token: str) -> str:
    return f"refresh:{token}"


def _verify_key(token: str) -> str:
    return f"verify:{token}"


def _store_token(key: str, token: str, expire: timedelta, payload: dict):
    redis_client.setex(key, expire, json.dumps(payload))


def _load_token(key: str):
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def _delete_token(key: str):
    redis_client.delete(key)


def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, JWT_SECRET_ACCESS, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    if not token:
        raise UnauthorizedException("Missing access token")
    try:
        return jwt.decode(token, JWT_SECRET_ACCESS, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedException("Invalid access token")


def create_refresh_token(data: dict, remember: bool) -> str:
    refresh_days = REFRESH_EXPIRE_DAYS_LONG if remember else REFRESH_EXPIRE_DAYS_SHORT
    expire = datetime.utcnow() + timedelta(days=refresh_days)

    to_encode = {**data, "exp": expire, "jti": secrets.token_hex(16)}
    token = jwt.encode(to_encode, JWT_SECRET_REFRESH, algorithm=ALGORITHM)

    _store_token(_refresh_key(token), token, timedelta(days=refresh_days), to_encode)
    return token


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_REFRESH, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedException("Invalid refresh token")

    data = _load_token(_refresh_key(token))
    if not data:
        raise UnauthorizedException("Refresh token expired or revoked")

    return payload


def invalidate_refresh_token(token: str):
    _delete_token(_refresh_key(token))


def create_verification_token(email: str, password: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=VERIFY_EXPIRE_MINUTES)
    payload = {
        "email": email,
        "password": password,
        "exp": expire,
        "jti": secrets.token_hex(16),
    }
    token = jwt.encode(payload, JWT_SECRET_VERIFY, algorithm=ALGORITHM)

    _store_token(
        _verify_key(token), token, timedelta(minutes=VERIFY_EXPIRE_MINUTES), payload
    )
    return token


def verify_verification_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET_VERIFY, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedException("Invalid verification token")

    data = _load_token(_verify_key(token))
    if not data:
        raise UnauthorizedException("Verification token expired or revoked")
    return payload


def invalidate_verification_token(token: str):
    _delete_token(_verify_key(token))


def generate_tokens(
    user_id: str, email: str, role: str = "user", remember: bool = False
):
    user_data = {"id": user_id, "email": email, "role": role, "remember": remember}
    return create_access_token(user_data), create_refresh_token(user_data, remember)


def rotate_refresh_token(old_refresh: str):
    payload = verify_refresh_token(old_refresh)
    user_data = {k: payload[k] for k in ("id", "email", "role", "remember")}

    access_token = create_access_token(user_data)
    _delete_token(_refresh_key(old_refresh))
    new_refresh = create_refresh_token(user_data, user_data["remember"])
    return access_token, new_refresh, payload["email"]
