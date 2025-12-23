from typing import Any, Dict, Iterable, Optional

from beanie import PydanticObjectId
from pymongo.errors import DuplicateKeyError

from templates.userTemplate import User
from utilities.logger import logger

from .baseRepository import BaseRepository


class UserRepository(BaseRepository):
    """
    MongoDB User repository.

    All operations are protected by:
      - retry logic
      - circuit breaker
      - transient error handling
    """

    async def create(
        self,
        *,
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
            return await self.executeAsync(op)
        except DuplicateKeyError:
            logger.warning("[UserRepository] Duplicate key while creating user")
            raise

    async def update(
        self,
        user_id: PydanticObjectId,
        data: Dict[str, Any],
    ) -> Optional[User]:
        if not data:
            return await self.get_by_id(user_id)

        async def op():
            data["updated_at"] = User.updated_at.default_factory()

            result = await User.find_one(User.id == user_id).update({"$set": data})

            if result.modified_count == 0:
                return None

            return await User.get(user_id)

        return await self.executeAsync(op)

    async def delete(self, user_id: PydanticObjectId) -> bool:
        async def op():
            user = await User.get(user_id)
            if not user:
                return False

            await user.delete()
            return True

        return await self.executeAsync(op)

    async def getById(self, user_id: PydanticObjectId) -> Optional[User]:
        return await self.executeAsync(lambda: User.get(user_id))

    async def getAll(self) -> Iterable[User]:
        return await self.executeAsync(lambda: User.find_all().to_list())

    async def getByEmail(self, email: str) -> Optional[User]:
        return await self.executeAsync(lambda: User.find_one(User.email == email))

    async def getByGoogleId(self, google_id: str) -> Optional[User]:
        return await self.executeAsync(
            lambda: User.find_one(User.google_id == google_id)
        )

    async def getByMicrosoftId(self, microsoft_id: str) -> Optional[User]:
        return await self.executeAsync(
            lambda: User.find_one(User.microsoft_id == microsoft_id)
        )
