from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from utilities.errorRaiser import UnauthorizedException, ForbiddenException
from service.cacheService import CacheService
from config.envConfig import settings


class BasicTokenService:
    def __init__(self):
        self.algorithm = settings.algorithm

        self.JWT_SECRET_ACCESS = settings.jwt_secret_access

        self.ACCESS_EXPIRE_MINUTES = 15

        self.require_auth_token = OAuth2PasswordBearer(tokenUrl="token")


    def decode_access_token(self, token: str) -> dict:
        if not token:
            raise UnauthorizedException("Missing access token")
        try:
            return jwt.decode(
                token, self.JWT_SECRET_ACCESS, algorithms=[self.algorithm]
            )
        except JWTError:
            raise UnauthorizedException("Invalid access token")

