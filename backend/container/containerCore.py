from resources.mongo_client import init_mongo
from resources.redis_client import init_redis
from utilities.logger import logger


async def init_connections():
    try:
        await init_redis()
        await init_mongo()
        logger.info("[Container] Core connections succeeded")
    except Exception as e:
        logger.error(f"[Container] Connections failed: {e}")
        raise
