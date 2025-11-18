import motor.motor_asyncio
from beanie import init_beanie

from config.environmentConfig import settings
from schema.mongo_template import (
    Category,
    Food,
    Reservation,
    Restaurant,
    Review,
    Survey,
)
from utilities.logger import logger

_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
db = _client.get_default_database()


async def init_mongo():
    try:
        await init_beanie(
            database=db,
            document_models=[Category, Restaurant, Food, Review, Reservation, Survey],
        )
        # logger.info("MongoDB (Beanie) initialized successfully.")
    except Exception as e:
        logger.error(f"MongoDB initialization failed: {e}")
        raise


mongo_client = _client
