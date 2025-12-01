from typing import Any, Dict, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from resources.database_client import get_db
from schema.psql_template import User
from utilities.logger import logger


class UserRepository:
    def __init__(self, db_factory=get_db):
        self.db_factory = db_factory

    async def create(
        self,
        email: str,
        provider: str,
        role: str,
        password: Optional[str] = None,
        microsoft_id: Optional[str] = None,
        google_id: Optional[str] = None,
        username: Optional[str] = None,
        name: Optional[str] = None,
        avatar: Optional[str] = None,
    ) -> User:
        try:
            async with self.db_factory() as db:
                user = User(
                    email=email,
                    provider=provider,
                    role=role,
                    password=password,
                    microsoft_id=microsoft_id,
                    google_id=google_id,
                    username=username,
                    name=name,
                    avatar=avatar,
                )

                db.add(user)
                await db.flush()
                await db.refresh(user)
                return user

        except IntegrityError as e:
            logger.error(f"[UserRepository] create failed - integrity error: {e}")
            raise e
        except Exception as e:
            logger.error(f"[UserRepository] create failed: {e}")
            raise e

    async def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:
        try:
            async with self.db_factory() as db:
                await db.execute(update(User).where(User.id == user_id).values(**data))

                result = await db.execute(select(User).where(User.id == user_id))
                return result.scalar_one_or_none()

        except Exception as e:
            logger.error(f"[UserRepository] update failed: {e}")
            raise e

    async def delete(self, user_id: int) -> bool:
        try:
            async with self.db_factory() as db:
                await db.execute(delete(User).where(User.id == user_id))
                return True

        except Exception as e:
            logger.error(f"[UserRepository] delete failed: {e}")
            raise e

    async def getById(self, id: int) -> Optional[User]:
        try:
            async with self.db_factory() as db:
                result = await db.execute(select(User).where(User.id == id))
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"[UserRepository] getById failed: {e}")
            raise e

    async def getAll(self):
        try:
            async with self.db_factory() as db:
                result = await db.execute(select(User))
                return result.scalars().all()
        except Exception as e:
            logger.error(f"[UserRepository] getAll failed: {e}")
            raise e

    async def getByEmail(self, email: str) -> Optional[User]:
        try:
            async with self.db_factory() as db:
                result = await db.execute(select(User).where(User.email == email))
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"[UserRepository] getByEmail failed: {e}")
            raise e

    async def getByGoogleId(self, google_id: str) -> Optional[User]:
        try:
            async with self.db_factory() as db:
                result = await db.execute(
                    select(User).where(User.google_id == google_id)
                )
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"[UserRepository] getByGoogleId failed: {e}")
            raise e

    async def getByMicrosoftId(self, microsoft_id: str) -> Optional[User]:
        try:
            async with self.db_factory() as db:
                result = await db.execute(
                    select(User).where(User.microsoft_id == microsoft_id)
                )
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"[UserRepository] getByMicrosoftId failed: {e}")
            raise e
