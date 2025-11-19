from datetime import timedelta
from typing import Optional

from fastapi import UploadFile

from schema.mongo_template import Restaurant
from service.baseService import BaseService
from service.cacheService import CacheService
from service.categoryService import CategoryService
from service.fileService import FileService
from service.userService import UserService
from utilities.errorRaiser import (
    AppHttpException,
    InternalErrorException,
    NotFoundException,
)
from utilities.logger import logger


class RestaurantService(BaseService):
    def __init__(
        self,
        cache_service: CacheService,
        user_service: Optional[UserService] = None,
        category_service: Optional[CategoryService] = None,
        file_service: Optional[FileService] = None,
        ttl_seconds: int = 300,
    ):
        self.user_service = user_service
        self.category_service = category_service
        self.cache_service = cache_service
        self.file_service = file_service
        self.ttl = ttl_seconds

    def _key_all(self) -> str:
        return "restaurant:all"

    def _key_one(self, cid: str) -> str:
        return f"restaurant:{cid}"

    async def getRestaurants(self):
        try:
            key = self._key_all()
            cached = self.cache_service.get(key)

            if cached:
                return self.cache_service.decodeModel(cached, Restaurant)

            restaurants = await Restaurant.find_all().to_list()

            self.cache_service.set(
                key,
                restaurants,
                expire=timedelta(seconds=self.ttl),
            )
            return restaurants

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(
                f"[RestaurantService] getRestaurants failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    async def getRestaurant(self, restaurant_id):
        try:
            key = self._key_one(restaurant_id)
            cached = self.cache_service.get(key)
            if cached:
                return self.cache_service.decodeModel(cached, Restaurant)

            restaurant = await Restaurant.get(restaurant_id)
            if not restaurant:
                raise NotFoundException(f"Restaurant '{restaurant_id}' does not exist")

            self.cache_service.set(key, restaurant, expire=self.ttl)
            return restaurant

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(
                f"[RestaurantService] getRestaurant failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    async def deleteRestaurant(self):
        try:
            self.ensureDependencies("file_service")

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(
                f"[RestaurantService] deleteRestaurant failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    async def createRestaurant(
        self,
        user_id: int,
        name: str,
        description: str,
        location: str,
        image: UploadFile,
    ):
        try:
            self.ensureDependencies("user_service", "category_service", "file_service")

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(
                f"[RestaurantService] createRestaurant failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")

    async def updateRestaurant(self):
        try:
            self.ensureDependencies("category_service", "file_service")

        except AppHttpException:
            raise

        except Exception as e:
            logger.error(
                f"[RestaurantService] updateRestaurant failed: {e}", exc_info=True
            )
            raise InternalErrorException("Internal server error")
