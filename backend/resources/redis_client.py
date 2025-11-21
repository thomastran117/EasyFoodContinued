import redis

from config.environmentConfig import settings
from utilities.logger import logger

REDIS_URL = settings.redis_url
MODE = settings.mode

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)


async def init_redis():
    try:
        if MODE in {"ci", "testing", "test"}:
            logger.info(f"Skipping Redis connection (mode={MODE})")

        redis_client.ping()
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise
