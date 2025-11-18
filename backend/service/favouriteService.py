from service.baseService import BaseService
from service.cacheService import CacheService
from service.restaurantService import RestaurantService
from service.userService import UserService


class FavouriteService:
    def __init__(
        self,
        user_service: UserService,
        restaurant_service: RestaurantService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.user_service = user_service
        self.restaurant_service = restaurant_service
        self.cache = cache_service
        self.ttl = ttl_seconds
