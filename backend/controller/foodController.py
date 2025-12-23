from service.foodService import FoodService


class FoodController:
    def __init__(self, foodservice: FoodService):
        self.food_service = foodservice
