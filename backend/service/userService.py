from fastapi import UploadFile

from resources.database_client import get_db
from schema.template import User
from service.fileService import (
    delete_uploaded_file,
    get_uploaded_file,
    save_upload_file,
)
from utilities.errorRaiser import BadRequestException, NotFoundException


def get_user_by_id(user_id: int):
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found.")
        return user


def update_avatar(image: UploadFile):
    with get_db() as db:
        pass


def update_user(
    db,
    user_id: int,
    username: str = None,
    phone: str = None,
    address: str = None,
    description: str = None,
):
    with get_db() as db:
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


def delete_user(db, user_id: int):
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("User not found.")

        db.delete(user)
        db.commit()
