from typing import Optional

from service.baseService import BaseService
from service.cacheService import CacheService
from service.categoryService import CategoryService
from service.fileService import FileService
from service.userService import UserService
from utilities.errorRaiser import InternalErrorExpection, ServiceUnavaliableException
from utilities.logger import logger


class RestaurantService:
    def __init__(
        self,
        cache_service: CacheService,
        user_service: Optional[UserService] = None,
        category_service: Optional[CategoryService] = None,
        file_service: Optional[FileService] = None,
    ):
        self.user_service = user_service
        self.category_service = category_service
        self.cache_service = cache_service
        self.file_service = file_service

    async def getRestaurants(self):
        pass

    async def getRestaurant(self):
        pass

    async def deleteRestaurant(self):
        try:
            if not self.user_service:
                logger.error(
                    "[RestaurantService] deleteRestaurant failed. UserService is not avaliable"
                )
                raise ServiceUnavaliableException(
                    "Restaurant is not ready to handle this request"
                )
            if not self.category_service:
                logger.error(
                    "[RestaurantService] deleteRestaurant failed. CategoryService is not avaliable"
                )
                raise ServiceUnavaliableException(
                    "Restaurant is not ready to handle this request"
                )
            if not self.file_service:
                logger.error(
                    "[RestaurantService] deleteRestaurant failed. FileService is not avaliable"
                )
                raise ServiceUnavaliableException(
                    "Restaurant is not ready to handle this request"
                )

        except ServiceUnavaliableException:
            raise

        except Exception as e:
            logger.error(f"[RestaurantService] deleteRestaurant failed error: {e}")
            raise InternalErrorExpection(
                "Restaurant deletion failed"
            )  # your own 500 wrapper

    async def createRestaurant(self):
        pass

    async def updateRestaurant(self):
        pass
