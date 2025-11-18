from typing import Literal

from service.basicTokenService import BasicTokenService
from service.cacheService import CacheService
from service.emailService import EmailService
from service.fileService import FileService

Lifetime = Literal["singleton", "transient", "scoped"]


def register_singletons(
    container,
    *,
    cache_lifetime: Lifetime = "singleton",
    email_lifetime: Lifetime = "singleton",
    file_lifetime: Lifetime = "singleton",
    basic_token_service_lifetime: Lifetime = "singleton",
):
    """Registers fundamental singletons (cache, email, file, token)."""
    container.register("CacheService", lambda c: CacheService(), cache_lifetime)
    container.register("EmailService", lambda c: EmailService(), email_lifetime)
    container.register("FileService", lambda c: FileService(), file_lifetime)
    container.register(
        "BasicTokenService",
        lambda c: BasicTokenService(),
        basic_token_service_lifetime,
    )
    return container
