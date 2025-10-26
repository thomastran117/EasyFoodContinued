from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utilities.errorRaiser import UnauthorizedException, ForbiddenException
from service.tokenService import TokenService

require_auth_token = OAuth2PasswordBearer(tokenUrl="/auth/login")
local_token_service = TokenService()


def get_current_user(token: str = Depends(require_auth_token)):
    """Extract and validate current user from the JWT access token."""

    payload = local_token_service.decode_access_token(token)
    required = ("id", "email", "role")
    if not all(payload.get(f) for f in required):
        raise UnauthorizedException("Invalid token payload")
    return {f: payload[f] for f in required}


def require_role(*roles: str):
    """Dependency that restricts access based on user roles."""

    def role_dependency(user: dict = Depends(get_current_user)):
        role = user.get("role")
        if role not in roles:
            raise ForbiddenException(
                f"Insufficient privileges: requires {roles}, found '{role}'"
            )
        return user

    return role_dependency
