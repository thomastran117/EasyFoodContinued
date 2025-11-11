import redis

from config.environmentConfig import settings
from utilities.logger import logger

REDIS_URL = settings.redis_url
MODE = settings.mode

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

try:

    if MODE in {"ci", "testing", "test"}:
        logger.info(f"Skipping Redis connection (mode={MODE})")
    else:
        redis_client.ping()
        logger.info("Redis connected successfully")

except:
    logger.error("Redis connection failed")
    raise
