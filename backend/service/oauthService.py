import httpx
from google.auth.transport import requests
from google.oauth2 import id_token
from jose import jwt as jose_jwt

from config.environmentConfig import settings
from utilities.errorRaiser import (
    AppHttpException,
    BadRequestException,
    InternalErrorException,
    UnauthorizedException,
)
from utilities.logger import logger


class OAuthService:
    def __init__(self):
        pass

    async def verifyMicrosoftToken(self, token: str):
        try:
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
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(
                f"[OAuthService] verifyMicrosoftToken failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal Server Error")

    async def verifyGoogleToken(self, token: str):
        try:
            request = requests.Request()
            clock_skew = 30

            idinfo = id_token.verify_oauth2_token(
                token,
                request,
                audience=settings.google_client_id,
                clock_skew_in_seconds=clock_skew,
            )

            if idinfo.get("iss") not in (
                "accounts.google.com",
                "https://accounts.google.com",
            ):
                raise UnauthorizedException("Invalid Google token issuer.")

            return (
                idinfo.get("email"),
                idinfo.get("name"),
                idinfo.get("picture"),
                idinfo.get("sub"),
            )

        except ValueError as e:
            if "early" in str(e) or "iat" in str(e):
                import asyncio

                await asyncio.sleep(0.5)

                try:
                    idinfo = id_token.verify_oauth2_token(
                        token,
                        requests.Request(),
                        audience=settings.google_client_id,
                        clock_skew_in_seconds=30,
                    )
                    return (
                        idinfo.get("email"),
                        idinfo.get("name"),
                        idinfo.get("picture"),
                        idinfo.get("sub"),
                    )
                except Exception:
                    raise UnauthorizedException("Google OAuth token not yet valid.")

            raise UnauthorizedException(f"Invalid Google token: {str(e)}")

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(f"[OAuthService] verifyGoogleToken failed: {e}", exc_info=True)
            raise InternalErrorException("Internal Server Error")
