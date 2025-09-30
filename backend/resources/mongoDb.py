import motor.motor_asyncio
from beanie import init_beanie
from config.envConfig import settings
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr
import asyncio
from utilities.logger import get_logger

logger = get_logger(__name__)


class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore
    name: Optional[str] = None
    role: str = "user"

    class Settings:
        name = "users"


_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)

try:
    asyncio.get_event_loop().run_until_complete(_client.admin.command("ping"))
    logger.info("MongoDB connected successfully")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    raise

db = _client.get_default_database()

try:
    asyncio.get_event_loop().run_until_complete(
        init_beanie(database=db, document_models=[User])
    )
    logger.info("Beanie ODM initialized successfully")
except Exception as e:
    logger.error(f"Beanie initialization failed: {e}")
    raise

mongo_client = _client
