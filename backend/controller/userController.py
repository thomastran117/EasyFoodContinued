from fastapi import APIRouter, Depends, HTTPException

from dtos.userDtos import UpdateUserDto
from resources.database_client import SessionLocal
from service.userService import UserService
from utilities.errorRaiser import raise_error
from common.authGuard import require_auth_token, get_current_user


class UserController:
    def __init__(self, user_service: UserService):
        """
        auth_service: instance of AuthService (which uses TokenService internally)
        """
        self.user_service = user_service

    async def get_user(self, id: int):
        try:
            user = self.user_service.get_user(user_id=id)
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "phone": user.phone,
                "address": user.address,
                "description": user.description,
                "profileUrl": user.profileUrl,
            }
        except Exception as e:
            raise_error(e)

    async def update_user(
        self, update: UpdateUserDto, token: str = Depends(require_auth_token)
    ):
        try:
            user_payload = get_current_user(token)
            updated_user = self.user_service.update_user(
                user_payload["id"],
                username=update.username,
                phone=update.phone,
                address=update.address,
                profileUrl=update.profileUrl,
                description=update.description,
            )
            return {"message": "User updated successfully", "user_id": updated_user.id}
        except Exception as e:
            raise_error(e)

    async def delete_user(self, token: str = Depends(require_auth_token)):
        try:
            user_payload = get_current_user(token)
            self.user_service.delete_user(user_payload["id"])
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise_error(e)
