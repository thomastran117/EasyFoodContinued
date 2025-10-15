from resources.schema import User
from utilities.errorRaiser import NotFoundException, BadRequestException
from utilities.imageValidator import is_valid_image_url


def get_user_by_id(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found.")
    return user


def update_user(
    db,
    user_id: int,
    username: str = None,
    phone: str = None,
    address: str = None,
    description: str = None,
    profileUrl: str = None,
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found.")

    if not is_valid_image_url(profileUrl):
        raise BadRequestException("Invalid profile URL")

    if username is not None:
        user.username = username
    if phone is not None:
        user.phone = phone
    if address is not None:
        user.address = address
    if description is not None:
        user.description = description
    if profileUrl is not None:
        user.profileUrl = profileUrl

    db.commit()
    db.refresh(user)
    return user


def delete_user(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found.")

    db.delete(user)
    db.commit()
