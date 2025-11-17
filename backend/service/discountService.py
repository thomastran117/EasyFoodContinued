from service.cacheService import CacheService
from service.foodService import FoodService
from service.drinkService import DrinkService
from service.comboService import ComboService


class DiscountService:
    def __init__(
        self,
        combo_service: ComboService,
        food_service: FoodService,
        drink_service: DrinkService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.combo_service = combo_service
        self.food_service = food_service
        self.drink_service = drink_service
        self.cache = cache_service
        self.ttl = ttl_seconds
