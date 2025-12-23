import motor.motor_asyncio
from beanie import init_beanie

from config.environmentConfig import settings
from templates.categoryTemplate import Category
from templates.restaurantTemplate import Restaurant
from templates.userTemplate import User
from utilities.logger import logger

_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db = _client.get_default_database()


async def init_mongo():
    try:
        await init_beanie(
            database=db,
            document_models=[Category, Restaurant, User],
        )
    except Exception as e:
        logger.error(f"MongoDB initialization failed: {e}")
        raise


mongo_client = _client
