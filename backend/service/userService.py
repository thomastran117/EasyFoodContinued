from fastapi import UploadFile

from resources.database_client import get_db
from schema.template import User
from service.fileService import FileService
from utilities.errorRaiser import BadRequestException, NotFoundException


class UserService:
    def __init__(
        self,
        file_service: FileService,
        db_factory=get_db,
    ):
        self.file_service = file_service
        self.db_factory = db_factory

    def get_user(self, user_id: int):
        with self.db_factory() as db:
            user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found.")
        return user

    def update_avatar(self, image: UploadFile):
        with self.db_factory() as db:
            pass

    def update_user(
        self,
        user_id: int,
        username: str = None,
        phone: str = None,
        address: str = None,
        description: str = None,
    ):
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

    def delete_user(self, user_id: int):
        with self.db_factory() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundException("User not found.")

            db.delete(user)
            db.commit()
