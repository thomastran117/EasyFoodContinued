from service.cacheService import CacheService


class CategoryService:
    def __init__(self, cache_service: CacheService):
        self.cache_service = cache_service
