from service.cacheService import CacheService
from service.userService import UserService


class DeliveryService:
    def __init__(
        self,
        user_service: UserService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.cache = cache_service
        self.ttl = ttl_seconds
