import json
import secrets
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.environmentConfig import settings
from service.cacheService import CacheService
from utilities.errorRaiser import (
    AppHttpException,
    InternalErrorException,
    UnauthorizedException,
)
from utilities.logger import logger


class TokenService:
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
        self.algorithm = settings.algorithm

        self.JWT_SECRET_ACCESS = settings.secret_key

        self.ACCESS_EXPIRE_MINUTES = 15
        self.REFRESH_EXPIRE_DAYS_SHORT = 1
        self.REFRESH_EXPIRE_DAYS_LONG = 7
        self.VERIFY_EXPIRE_MINUTES = 60

        self.require_auth_token = OAuth2PasswordBearer(tokenUrl="token")

    def createAccessToken(self, data: dict) -> str:
        try:
            expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_EXPIRE_MINUTES)
            to_encode = {**data, "exp": expire}
            return jwt.encode(
                to_encode, self.JWT_SECRET_ACCESS, algorithm=self.algorithm
            )
        except Exception as e:
            logger.error(f"[TokenService] createAccessToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def verifyAccessToken(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.JWT_SECRET_ACCESS,
                algorithms=[self.algorithm],
            )
        except JWTError:
            raise UnauthorizedException("Invalid or expired access token")
        except Exception as e:
            logger.error(f"[TokenService] verifyAccessToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def _generateOpaque(self) -> str:
        return secrets.token_hex(64)

    def createRefreshToken(self, user_data: dict, remember: bool) -> str:
        try:
            refresh_days = (
                self.REFRESH_EXPIRE_DAYS_LONG
                if remember
                else self.REFRESH_EXPIRE_DAYS_SHORT
            )

            token = self._generateOpaque()
            expire_at = datetime.utcnow() + timedelta(days=refresh_days)

            redis_value = {
                "id": user_data["id"],
                "email": user_data["email"],
                "role": user_data["role"],
                "remember": remember,
                "exp": expire_at.isoformat(),
            }

            self.cache_service.set(
                f"refresh:{token}",
                json.dumps(redis_value),
                timedelta(days=refresh_days),
                redis_value,
            )

            return token

        except Exception as e:
            logger.error(
                f"[TokenService] createRefreshToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def verifyRefreshToken(self, token: str) -> dict:
        try:
            raw = self.cache_service.get(f"refresh:{token}")
            if not raw:
                raise UnauthorizedException("Refresh token expired or revoked")
            return json.loads(raw) if isinstance(raw, str) else raw

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] verifyRefreshToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def generateTokens(self, user_id: str, email: str, role="user", remember=False):
        try:
            user_data = {
                "id": user_id,
                "email": email,
                "role": role,
                "remember": remember,
            }

            access = self.createAccessToken(user_data)
            refresh = self.createRefreshToken(user_data, remember)

            return access, refresh
        except Exception as e:
            logger.error(f"[TokenService] generateTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def rotateTokens(self, old_refresh: str):
        try:
            payload = self.verifyRefreshToken(old_refresh)

            user_data = {
                "id": payload["id"],
                "email": payload["email"],
                "role": payload["role"],
                "remember": payload["remember"],
            }

            new_access = self.createAccessToken(user_data)
            new_refresh = self.createRefreshToken(user_data, user_data["remember"])

            self.cache_service.delete(f"refresh:{old_refresh}")

            return new_access, new_refresh, payload["email"]

        except Exception as e:
            logger.error(f"[TokenService] rotateTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def logoutToken(self, token: str):
        try:
            self.verifyRefreshToken(token)
            self.cache_service.delete(f"refresh:{token}")
        except Exception as e:
            logger.error(f"[TokenService] logoutToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def createVerificationToken(self, email: str, password: str) -> str:
        try:
            token = self._generateOpaque()
            expire_at = datetime.utcnow() + timedelta(
                minutes=self.VERIFY_EXPIRE_MINUTES
            )

            payload = {
                "email": email,
                "password": password,
                "exp": expire_at.isoformat(),
            }

            self.cache_service.set(
                f"verify:{token}",
                json.dumps(payload),
                timedelta(minutes=self.VERIFY_EXPIRE_MINUTES),
                payload,
            )

            return token

        except Exception as e:
            logger.error(
                f"[TokenService] createVerificationToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def verifyVerificationToken(self, token: str) -> dict:
        try:
            raw = self.cache_service.get(f"verify:{token}")

            if not raw:
                raise UnauthorizedException("Verification token expired or revoked")

            self.cache_service.delete(f"verify:{token}")

            return json.loads(raw) if isinstance(raw, str) else raw

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] verifyVerificationToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")
