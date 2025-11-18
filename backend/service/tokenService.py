import json
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from config.environmentConfig import settings
from service.basicTokenService import BasicTokenService
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

        self.JWT_SECRET_ACCESS = settings.jwt_secret_access
        self.JWT_SECRET_REFRESH = settings.jwt_secret_refresh
        self.JWT_SECRET_VERIFY = settings.jwt_secret_verify

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
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[TokenService] createAccessToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def createRefreshToken(self, data: dict, remember: bool) -> str:
        try:
            refresh_days = (
                self.REFRESH_EXPIRE_DAYS_LONG
                if remember
                else self.REFRESH_EXPIRE_DAYS_SHORT
            )
            expire = datetime.utcnow() + timedelta(days=refresh_days)

            to_encode = {**data, "exp": expire, "jti": secrets.token_hex(16)}
            token = jwt.encode(
                to_encode, self.JWT_SECRET_REFRESH, algorithm=self.algorithm
            )

            self.cache_service.set(
                f"refresh:{token}", token, timedelta(days=refresh_days), to_encode
            )
            return token
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] createRefreshToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def createVerificationToken(self, email: str, password: str) -> str:
        try:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=self.VERIFY_EXPIRE_MINUTES
            )
            payload = {
                "email": email,
                "password": password,
                "exp": expire,
                "jti": secrets.token_hex(16),
            }
            token = jwt.encode(
                payload, self.JWT_SECRET_VERIFY, algorithm=self.algorithm
            )
            self.cache_service.set(
                f"verify:{token}",
                token,
                timedelta(minutes=self.VERIFY_EXPIRE_MINUTES),
                payload,
            )
            return token
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] createVerificationToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def verifyAccessToken(self, token: str) -> dict:
        try:
            if not token:
                raise UnauthorizedException("Missing access token")
            return jwt.decode(
                token, self.JWT_SECRET_ACCESS, algorithms=[self.algorithm]
            )
        except JWTError:
            raise UnauthorizedException("Invalid access token")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[TokenService] verifyAccessToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def verifyRefreshToken(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.JWT_SECRET_REFRESH, algorithms=[self.algorithm]
            )
            data = self.cache_service.get(f"refresh:{token}")

            if not data:
                raise UnauthorizedException("Refresh token expired or revoked")

            return payload

        except JWTError:
            raise UnauthorizedException("Invalid refresh token")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] verifyRefreshToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def verifyVerificationToken(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.JWT_SECRET_VERIFY, algorithms=[self.algorithm]
            )
            data = self.cache_service.get(f"verify:{token}")

            if not data:
                raise UnauthorizedException("Verification token expired or revoked")

            self.cache_service.delete(f"verify:{token}")
            return payload
        except JWTError:
            raise UnauthorizedException("Invalid verification token")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[TokenService] verifyVerificationToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    def generateTokens(
        self, user_id: str, email: str, role: str = "user", remember: bool = False
    ):
        try:
            user_data = {
                "id": user_id,
                "email": email,
                "role": role,
                "remember": remember,
            }
            return self.createAccessToken(user_data), self.createRefreshToken(
                user_data, remember
            )
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[TokenService] generateTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def rotateTokens(self, old_refresh: str):
        try:
            payload = self.verifyRefreshToken(old_refresh)
            user_data = {k: payload[k] for k in ("id", "email", "role", "remember")}
            access_token = self.createAccessToken(user_data)
            self.cache_service.delete(f"refresh:{old_refresh}")
            new_refresh = self.createRefreshToken(user_data, user_data["remember"])
            return access_token, new_refresh, payload["email"]
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[TokenService] rotateTokens failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def logoutToken(self, token):
        try:
            self.verifyRefreshToken(token)
            self.cache_service.delete(f"refresh:{token}")
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[TokenService] logoutToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
