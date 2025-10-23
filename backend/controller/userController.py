from fastapi import APIRouter, Depends, HTTPException

from dtos.userDtos import UpdateUserDto
from resources.database_client import SessionLocal
from service.tokenService import get_current_user, require_auth_token
from service.userService import delete_user, get_user_by_id, update_user
from utilities.errorRaiser import raise_error


async def get_user(id: int):
    db = SessionLocal()
    try:
        user = get_user_by_id(db, user_id=id)
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
    finally:
        db.close()


async def get_me(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        user = get_user_by_id(db, user_id=user_payload["id"])
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
    finally:
        db.close()


async def update_me(update: UpdateUserDto, token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        updated_user = update_user(
            db,
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
    finally:
        db.close()


async def delete_me(token: str = Depends(require_auth_token)):
    db = SessionLocal()
    try:
        user_payload = get_current_user(token)
        delete_user(db, user_payload["id"])
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise_error(e)
    finally:
        db.close()
