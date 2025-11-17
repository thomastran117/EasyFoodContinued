from service.foodService import FoodService


class FoodController:
    def __init__(self, food_service: FoodService):
        self.food_service = food_service
