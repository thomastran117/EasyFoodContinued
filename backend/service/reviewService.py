from service.baseService import BaseService
from service.cacheService import CacheService
from service.restaurantService import RestaurantService


class ReviewService:
    def __init__(
        self,
        restaurant_service: RestaurantService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.restaurant_service = restaurant_service
        self.cache = cache_service
        self.ttl = ttl_seconds
