from pathlib import Path
from typing import Optional

from beanie import PydanticObjectId
from fastapi import UploadFile

from repository.userRepository import UserRepository
from service.fileService import FileService
from utilities.errorRaiser import (
    AppHttpException,
    InternalErrorException,
    NotFoundException,
)
from utilities.logger import logger


class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        file_service: FileService,
    ):
        self.user_repository = user_repository
        self.file_service = file_service

    async def getUser(self, user_id: PydanticObjectId):
        try:
            user = await self.user_repository.getById(user_id)
            if not user:
                raise NotFoundException("User not found.")
            return user

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] getUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def updateUser(
        self,
        user_id: PydanticObjectId,
        username: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
    ):
        try:
            data = {}

            if username is not None:
                data["username"] = username
            if phone is not None:
                data["phone"] = phone
            if address is not None:
                data["address"] = address
            if description is not None:
                data["description"] = description

            if not data:
                return await self.getUser(user_id)

            user = await self.user_repository.update(user_id, data)
            if not user:
                raise NotFoundException("User not found.")

            return user

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] updateUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def deleteUser(self, user_id: PydanticObjectId):
        try:
            deleted = await self.user_repository.delete(user_id)
            if not deleted:
                raise NotFoundException("User not found.")

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] deleteUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def updateAvatar(self, user_id: PydanticObjectId, file: UploadFile) -> str:
        """
        Upload avatar, update DB record, and remove old one if exists.
        """
        try:
            user = await self.user_repository.getById(user_id)
            if not user:
                raise NotFoundException("User not found")

            if user.avatar:
                try:
                    old_filename = Path(user.avatar).name
                    self.file_service.deleteUploadFile("users", old_filename)
                except Exception:
                    pass

            avatar_path = await self.file_service.handleUploadFile(file, "users")

            updated_user = await self.user_repository.update(
                user_id,
                {"avatar": avatar_path},
            )

            if not updated_user:
                raise NotFoundException("User not found")

            return avatar_path

        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] updateAvatar failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
