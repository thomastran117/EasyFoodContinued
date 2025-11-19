from pathlib import Path

from fastapi import UploadFile

from resources.database_client import get_db
from schema.psql_template import User
from service.baseService import BaseService
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
        file_service: FileService,
        db_factory=get_db,
    ):
        self.file_service = file_service
        self.db_factory = db_factory

    def getUser(self, user_id: int):
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundException("User not found.")
            return user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] getUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def updateUser(
        self,
        user_id: int,
        username: str = None,
        phone: str = None,
        address: str = None,
        description: str = None,
    ):
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise NotFoundException("User not found.")

                if username is not None:
                    user.username = username
                if phone is not None:
                    user.phone = phone
                if address is not None:
                    user.address = address
                if description is not None:
                    user.description = description

                db.commit()
                db.refresh(user)
                return user
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] updateUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    def deleteUser(self, user_id: int):
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise NotFoundException("User not found.")

                db.delete(user)
                db.commit()
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] deleteUser failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")

    async def updateAvatar(self, user_id: int, file: UploadFile) -> str:
        """Upload avatar, update DB record, and remove old one if exists."""
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise NotFoundException("User not found")

                if user.avatar:
                    try:
                        old_filename = Path(user.avatar).name
                        self.file_service.deleteUploadFile("users", old_filename)
                    except Exception:
                        pass

                avatar_path = await self.file_service.handleUploadFile(file, "users")

                user.avatar = avatar_path
                db.add(user)
                db.commit()
                db.refresh(user)

                return avatar_path
        except AppHttpException:
            raise
        except Exception as e:
            logger.error(f"[UserService] updateAvatar failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
