from service.fileService import FileService
from service.cacheService import CacheService


class RestaurantService:
    def __init__(self, cache_service: CacheService, file_service: FileService):
        self.cache_service = cache_service
        self.file_service = file_service
