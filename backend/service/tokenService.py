import json
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utilities.exception import UnauthorizedException
import secrets
from datetime import datetime, timedelta, timezone
from resource.redisDb import redis_client
from config.envConfig import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_MINUTES = settings.expire_minutes


def _token_key(token: str) -> str:
    return f"verify:{token}"


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        if token is None:
            raise UnauthorizedException("Missing token")
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise UnauthorizedException("Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_token(token)
    user_id = payload.get("id")
    email = payload.get("email")
    role = payload.get("role")

    if user_id is None or email is None or role is None:
        raise UnauthorizedException("Invalid token payload")

    return {"id": user_id, "email": email, "role": role}


def create_verification_token(email: str, password: str) -> str:
    token = secrets.token_urlsafe(32)
    payload = {
        "email": email,
        "password": password,
        "expires": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    redis_client.setex(_token_key(token), 900, json.dumps(payload))
    return token


def get_token_data(token: str):
    raw = redis_client.get(_token_key(token))
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def invalidate_token(token: str):
    redis_client.delete(_token_key(token))
