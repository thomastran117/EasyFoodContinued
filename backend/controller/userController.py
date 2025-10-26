from fastapi import Depends, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
import filetype
import io
import secrets
from dtos.userDtos import UpdateUserDto
from service.userService import UserService
from utilities.errorRaiser import raise_error
from common.authGuard import require_auth_token, get_current_user

MAX_FILE_SIZE = 10 * 1024 * 1024


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

    async def update_avatar(
        self,
        file: UploadFile = File(...),
        token: str = Depends(get_current_user),
    ):
        try:
            user = token

            data = await file.read()
            if len(data) > MAX_FILE_SIZE:
                raise HTTPException(
                    413, f"File exceeds {MAX_FILE_SIZE / (1024**2)} MB limit"
                )

            kind = filetype.guess(data)
            if not kind or kind.mime not in ["image/jpeg", "image/png"]:
                raise HTTPException(400, "Only JPG and PNG files are allowed")

            try:
                Image.open(io.BytesIO(data)).verify()
            except Exception:
                raise HTTPException(400, "Invalid or corrupted image")

            file.file.seek(0)

            avatar_path = await self.user_service.update_avatar(user["id"], file)
            return {"message": "Avatar updated successfully", "avatar": avatar_path}
        except Exception as e:
            raise_error(e)
