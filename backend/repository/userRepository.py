from typing import Any, Dict, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError

from resources.database_client import get_db
from schema.psql_template import User
from utilities.logger import logger

from .baseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db_factory=get_db):
        super().__init__()
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

        async def op():
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

        return await self.retry(op)

    async def update(self, user_id: int, data: Dict[str, Any]) -> Optional[User]:

        async def op():
            async with self.db_factory() as db:
                await db.execute(update(User).where(User.id == user_id).values(**data))
                result = await db.execute(select(User).where(User.id == user_id))
                return result.scalar_one_or_none()

        return await self.retry(op)

    async def delete(self, user_id: int) -> bool:

        async def op():
            async with self.db_factory() as db:
                await db.execute(delete(User).where(User.id == user_id))
                return True

        return await self.retry(op)

    async def getById(self, id: int) -> Optional[User]:

        async def op():
            async with self.db_factory() as db:
                result = await db.execute(select(User).where(User.id == id))
                return result.scalar_one_or_none()

        return await self.retry(op)

    async def getAll(self):
        async def op():
            async with self.db_factory() as db:
                result = await db.execute(select(User))
                return result.scalars().all()

        return await self.retry(op)

    async def getByEmail(self, email: str) -> Optional[User]:

        async def op():
            async with self.db_factory() as db:
                result = await db.execute(select(User).where(User.email == email))
                return result.scalar_one_or_none()

        return await self.retry(op)

    async def getByGoogleId(self, google_id: str) -> Optional[User]:

        async def op():
            async with self.db_factory() as db:
                result = await db.execute(
                    select(User).where(User.google_id == google_id)
                )
                return result.scalar_one_or_none()

        return await self.retry(op)

    async def getByMicrosoftId(self, microsoft_id: str) -> Optional[User]:

        async def op():
            async with self.db_factory() as db:
                result = await db.execute(
                    select(User).where(User.microsoft_id == microsoft_id)
                )
                return result.scalar_one_or_none()

        return await self.retry(op)
