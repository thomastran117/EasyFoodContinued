import httpx
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt as jose_jwt

from config.environmentConfig import settings
from utilities.errorRaiser import (
    BadRequestException,
    UnauthorizedException,
    ServiceUnavaliableException,
)


class OAuthService:
    def __init__(self):
        pass

    async def verifyMicrosoftToken(self, token: str):
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

        return email, user_id, name, picture

    async def verifyGoogleToken(self, token: str):
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                audience=(
                    settings.google_client_id if settings.google_client_id else None
                ),
            )

            if idinfo.get("iss") not in (
                "accounts.google.com",
                "https://accounts.google.com",
            ):
                raise UnauthorizedException("Invalid Google token issuer.")

            email = idinfo.get("email")
            name = idinfo.get("name")
            picture = idinfo.get("picture")
            user_id = idinfo.get("sub")
            return email, name, picture, user_id

        except ValueError as e:
            raise UnauthorizedException(f"Invalid Google token: {str(e)}")
        except Exception as e:
            raise ServiceUnavaliableException("Google OAuth Failed")
