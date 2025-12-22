from typing import Any, Dict, Optional

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from schema.mongo_template import User
from utilities.logger import logger

from .baseRepository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__()

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
            return await user.insert()

        try:
            return await self.retry(op)
        except DuplicateKeyError as e:
            logger.warning("Duplicate key error creating user")
            raise e

    async def update(
        self,
        user_id: PydanticObjectId,
        data: Dict[str, Any],
    ) -> Optional[User]:

        async def op():
            data["updated_at"] = (
                data.get("updated_at") or User.updated_at.default_factory()
            )

            user = await User.get(user_id)
            if not user:
                return None

            await user.update({"$set": data})
            return await User.get(user_id)

        return await self.retry(op)

    async def delete(self, user_id: PydanticObjectId) -> bool:

        async def op():
            user = await User.get(user_id)
            if not user:
                return False

            await user.delete()
            return True

        return await self.retry(op)

    async def getById(self, id: PydanticObjectId) -> Optional[User]:

        async def op():
            return await User.get(id)

        return await self.retry(op)

    async def getAll(self):

        async def op():
            return await User.find_all().to_list()

        return await self.retry(op)

    async def getByEmail(self, email: str) -> Optional[User]:

        async def op():
            return await User.find_one(User.email == email)

        return await self.retry(op)

    async def getByGoogleId(self, google_id: str) -> Optional[User]:

        async def op():
            return await User.find_one(User.google_id == google_id)

        return await self.retry(op)

    async def getByMicrosoftId(self, microsoft_id: str) -> Optional[User]:

        async def op():
            return await User.find_one(User.microsoft_id == microsoft_id)

        return await self.retry(op)
