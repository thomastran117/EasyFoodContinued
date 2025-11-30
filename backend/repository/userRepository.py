from resources.database_client import get_db
from schema.psql_template import User
from utilities.logger import logger


class UserRepository:
    def __init__(self, db_factory=get_db,):
        self.db_factory = db_factory

    async def create(
        self,
        email: str,
        provider: str,
        role: str,
        password: str,
        microsoft_id: str,
        google_id: str,
    ):
        try:
            pass
        except Exception as e:
            logger.error(f"[UserRepository] create failed: {e}")
            raise e

    async def update(self):
        try:
            pass
        except Exception as e:
            logger.error(f"[UserRepository] update failed: {e}")
            raise e

    async def delete(self):
        try:
            pass
        except Exception as e:
            logger.error(f"[UserRepository] delete failed: {e}")
            raise e

    async def getById(self, id: int):
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.id == id).first()
            return user
        except Exception as e:
            logger.error(f"[UserRepository] getById failed: {e}")
            raise e

    async def getAll(self):
        try:
            with self.db_factory() as db:
                users = db.query(User).all()
            return users
        except Exception as e:
            logger.error(f"[UserRepository] getAll failed: {e}")
            raise e

    async def getByEmail(self, email: str):
        try:
            with self.db_factory() as db:
                user = db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            logger.error(f"[UserRepository] getAll failed: {e}")
            raise e
