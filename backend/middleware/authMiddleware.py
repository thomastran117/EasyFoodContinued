from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from utilities.errorRaiser import UnauthorizedException, ForbiddenException

require_auth_token = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_token_service(request: Request):
    """
    Resolve TokenService from the IoC container stored in app.state.
    This replaces the old container import from containerEntry.
    """
    container = request.app.state.container
    token_service = await container.resolve("TokenService")
    return token_service


async def get_current_user(
    request: Request,
    token: str = Depends(require_auth_token),
    token_service=Depends(get_token_service),
):
    """
    Extract and validate the current user from the JWT access token.
    Uses the TokenService resolved from IoC container.
    """
    try:
        payload = token_service.decode_access_token(token)
    except JWTError:
        raise UnauthorizedException("Invalid or expired access token")

    required = ("id", "email", "role")
    if not all(payload.get(f) for f in required):
        raise UnauthorizedException("Invalid token payload")

    return {f: payload[f] for f in required}


def require_role(*roles: str):
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
