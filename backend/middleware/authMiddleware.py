from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from service.basicTokenService import BasicTokenService
from utilities.errorRaiser import ForbiddenException, UnauthorizedException, raise_error
from utilities.logger import logger

require_auth_token = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def getBasicTokenService(request: Request):
    """
    Resolve TokenService from the IoC container stored in app.state.
    This replaces the old container import from containerEntry.
    """
    try:
        container = request.app.state.container
        scope = request.state.scope

        controller = await container.resolve("BasicTokenService", scope)
        controller.request = request

        return controller

    except Exception as e:
        logger.error(f"[AuthMiddleware] Resolving BasicTokenService failed: {e}")
        raise_error(e)


async def get_current_user(
    request: Request,
    token: str = Depends(require_auth_token),
    token_service: BasicTokenService = Depends(getBasicTokenService),
):
    """
    Extract and validate the current user from the JWT access token.
    Uses the TokenService resolved from IoC container.
    """
    try:
        payload = token_service.decodeAccessToken(token)
    except JWTError:
        raise UnauthorizedException("Invalid or expired access token")

    required = ("id", "email", "role")
    if not all(payload.get(f) for f in required):
        raise UnauthorizedException("Invalid token payload")

    return {f: payload[f] for f in required}


def requireRole(*roles: str):
    """
    Dependency factory that restricts access based on user roles.
    Example: @router.get(..., dependencies=[Depends(require_role("admin"))])
    """

    async def role_dependency(user: dict = Depends(get_current_user)):
        role = user.get("role")
        if role not in roles:
            raise ForbiddenException(
                f"Insufficient privileges: requires {roles}, found '{role}'"
            )
        return user

    return role_dependency
