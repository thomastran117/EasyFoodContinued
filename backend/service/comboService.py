from service.cacheService import CacheService
from service.foodService import FoodService
from service.drinkService import DrinkService


class ComboService:
    def __init__(
        self,
        food_service: FoodService,
        drink_service: DrinkService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.food_service = food_service
        self.drink_service = drink_service
        self.cache = cache_service
        self.ttl = ttl_seconds
