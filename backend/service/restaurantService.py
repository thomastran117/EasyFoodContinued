from service.fileService import FileService
from service.cacheService import CacheService
from service.categoryService import CategoryService
from service.userService import UserService


class RestaurantService:
    def __init__(
        self,
        user_service: UserService,
        category_service: CategoryService,
        cache_service: CacheService,
        file_service: FileService,
    ):
        self.user_service = user_service
        self.category_service = category_service
        self.cache_service = cache_service
        self.file_service = file_service
