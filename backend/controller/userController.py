import io

import filetype
from fastapi import File, HTTPException, Request, UploadFile
from PIL import Image

from dtos.userDtos import UpdateUserDto
from service.userService import UserService
from utilities.errorRaiser import AppHttpException, raise_error
from utilities.logger import logger

MAX_FILE_SIZE = 10 * 1024 * 1024


class UserController:
    def __init__(self, userservice: UserService):
        self.user_service = userservice
        self.request: Request | None = None

    async def getUserByID(self, id: int):
        try:
            user = self.user_service.getUser(user_id=id)
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "phone": user.phone,
                "address": user.address,
                "description": user.description,
                "profileUrl": user.profileUrl,
            }
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[UserController] getUserByID failed: {e}")
            raise_error(e)

    async def updateUser(self, user_payload: dict, update: UpdateUserDto):
        try:
            updated_user = self.user_service.updateUser(
                user_payload["id"],
                username=update.username,
                phone=update.phone,
                address=update.address,
                profileUrl=update.profileUrl,
                description=update.description,
            )
            return {"message": "User updated successfully", "user_id": updated_user.id}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[UserController] updateAvatar failed: {e}")
            raise_error(e)

    async def deleteUser(self, user_payload: dict):
        try:
            self.user_service.deleteUser(user_payload["id"])
            return {"message": "User deleted successfully"}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[UserController] deleteUser failed: {e}")
            raise_error(e)

    async def updateAvatar(self, user_payload: dict, file: UploadFile):
        try:
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

            avatar_path = await self.user_service.updateAvatar(user_payload["id"], file)
            return {"message": "Avatar updated successfully", "avatar": avatar_path}
        except AppHttpException as e:
            raise_error(e)
        except Exception as e:
            logger.error(f"[UserController] updateAvatar failed: {e}")
            raise_error(e)
