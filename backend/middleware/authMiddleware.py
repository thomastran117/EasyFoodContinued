from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from utilities.errorRaiser import UnauthorizedException, ForbiddenException

require_auth_token = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token_service():
    """Lazy-load BasicTokenService from IoC container to avoid circular imports."""
    # ⬇️ Import here, not at module top
    from container.containerEntry import container

    return container.resolve("TokenService")


async def get_current_user(
    token: str = Depends(require_auth_token),
    token_service=Depends(get_token_service),
):
    """Extract and validate current user from the JWT access token using BasicTokenService."""
    try:
        payload = token_service.decode_access_token(token)
    except JWTError:
        raise UnauthorizedException("Invalid or expired access token")

    required = ("id", "email", "role")
    if not all(payload.get(f) for f in required):
        raise UnauthorizedException("Invalid token payload")

    return {f: payload[f] for f in required}


def require_role(*roles: str):
    """Dependency that restricts access based on user roles."""

    async def role_dependency(user: dict = Depends(get_current_user)):
        role = user.get("role")
        if role not in roles:
            raise ForbiddenException(
                f"Insufficient privileges: requires {roles}, found '{role}'"
            )
        return user

    return role_dependency
