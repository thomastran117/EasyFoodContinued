from service.baseService import BaseService
from service.cacheService import CacheService


class DriverService:
    def __init__(self, cache_service: CacheService, ttl_seconds: int = 300):
        self.cache = cache_service
        self.ttl = ttl_seconds
