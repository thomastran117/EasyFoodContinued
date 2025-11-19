from typing import Literal

from service.basicTokenService import BasicTokenService
from service.cacheService import CacheService
from service.fileService import FileService
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


def register_singletons(
    container,
    *,
    cache_lifetime: Lifetime = "singleton",
    file_lifetime: Lifetime = "singleton",
    basic_token_service_lifetime: Lifetime = "singleton",
):
    """Registers fundamental singletons (cache, email, file, token)."""
    try:
        container.register("CacheService", lambda c: CacheService(), cache_lifetime)
        container.register("FileService", lambda c: FileService(), file_lifetime)
        container.register(
            "BasicTokenService",
            lambda c: BasicTokenService(),
            basic_token_service_lifetime,
        )
        return container
    except Exception as e:
        logger.error(f"[Container] Singleton registration failed: {e}")
        raise
