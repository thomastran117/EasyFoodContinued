import json
import secrets
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.envConfig import settings
from resources.redis_client import redis_client
from utilities.errorRaiser import ForbiddenException, UnauthorizedException


class TokenService:
    def __init__(self, redis=redis_client):
        self.redis = redis
        self.algorithm = settings.algorithm

        self.JWT_SECRET_ACCESS = settings.jwt_secret_access
        self.JWT_SECRET_REFRESH = settings.jwt_secret_refresh
        self.JWT_SECRET_VERIFY = settings.jwt_secret_verify

        self.ACCESS_EXPIRE_MINUTES = 15
        self.REFRESH_EXPIRE_DAYS_SHORT = 1
        self.REFRESH_EXPIRE_DAYS_LONG = 7
        self.VERIFY_EXPIRE_MINUTES = 60

        self.require_auth_token = OAuth2PasswordBearer(tokenUrl="token")

    def _refresh_key(self, token: str) -> str:
        return f"refresh:{token}"

    def _verify_key(self, token: str) -> str:
        return f"verify:{token}"

    def _store_token(self, key: str, token: str, expire: timedelta, payload: dict):
        self.redis.setex(key, expire, json.dumps(payload))

    def _load_token(self, key: str):
        raw = self.redis.get(key)
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    def _delete_token(self, key: str):
        self.redis.delete(key)

    def create_access_token(self, data: dict) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_EXPIRE_MINUTES)
        to_encode = {**data, "exp": expire}
        return jwt.encode(to_encode, self.JWT_SECRET_ACCESS, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict, remember: bool) -> str:
        refresh_days = (
            self.REFRESH_EXPIRE_DAYS_LONG
            if remember
            else self.REFRESH_EXPIRE_DAYS_SHORT
        )
        expire = datetime.utcnow() + timedelta(days=refresh_days)

        to_encode = {**data, "exp": expire, "jti": secrets.token_hex(16)}
        token = jwt.encode(to_encode, self.JWT_SECRET_REFRESH, algorithm=self.algorithm)

        self._store_token(
            self._refresh_key(token), token, timedelta(days=refresh_days), to_encode
        )
        return token

    def create_verification_token(self, email: str, password: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.VERIFY_EXPIRE_MINUTES
        )
        payload = {
            "email": email,
            "password": password,
            "exp": expire,
            "jti": secrets.token_hex(16),
        }
        token = jwt.encode(payload, self.JWT_SECRET_VERIFY, algorithm=self.algorithm)
        self._store_token(
            self._verify_key(token),
            token,
            timedelta(minutes=self.VERIFY_EXPIRE_MINUTES),
            payload,
        )
        return token

    def decode_access_token(self, token: str) -> dict:
        if not token:
            raise UnauthorizedException("Missing access token")
        try:
            return jwt.decode(
                token, self.JWT_SECRET_ACCESS, algorithms=[self.algorithm]
            )
        except JWTError:
            raise UnauthorizedException("Invalid access token")

    def verify_refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.JWT_SECRET_REFRESH, algorithms=[self.algorithm]
            )
        except JWTError:
            raise UnauthorizedException("Invalid refresh token")

        data = self._load_token(self._refresh_key(token))
        if not data:
            raise UnauthorizedException("Refresh token expired or revoked")
        return payload

    def verify_verification_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.JWT_SECRET_VERIFY, algorithms=[self.algorithm]
            )
        except JWTError:
            raise UnauthorizedException("Invalid verification token")

        data = self._load_token(self._verify_key(token))
        if not data:
            raise UnauthorizedException("Verification token expired or revoked")
        return payload

    def invalidate_refresh_token(self, token: str):
        self._delete_token(self._refresh_key(token))

    def invalidate_verification_token(self, token: str):
        self._delete_token(self._verify_key(token))

    def generate_tokens(
        self, user_id: str, email: str, role: str = "user", remember: bool = False
    ):
        user_data = {"id": user_id, "email": email, "role": role, "remember": remember}
        return self.create_access_token(user_data), self.create_refresh_token(
            user_data, remember
        )

    def rotate_refresh_token(self, old_refresh: str):
        payload = self.verify_refresh_token(old_refresh)
        user_data = {k: payload[k] for k in ("id", "email", "role", "remember")}
        access_token = self.create_access_token(user_data)
        self._delete_token(self._refresh_key(old_refresh))
        new_refresh = self.create_refresh_token(user_data, user_data["remember"])
        return access_token, new_refresh, payload["email"]

    def get_current_user(
        self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))
    ):
        payload = self.decode_access_token(token)
        required = ("id", "email", "role")
        if not all(payload.get(f) for f in required):
            raise UnauthorizedException("Invalid token payload")
        return {f: payload[f] for f in required}

    def require_role(self, *roles: str):
        def role_dependency(user: dict = Depends(self.get_current_user)):
            role = user.get("role")
            if role not in roles:
                raise ForbiddenException(
                    f"Insufficient privileges: requires {roles}, found '{role}'"
                )
            return user

        return role_dependency
