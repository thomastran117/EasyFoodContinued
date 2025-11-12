from service.restaurantService import RestaurantService


class RestaurantController:
    def __init__(self, restaurant_service: RestaurantService):
        self.restaurant_service = restaurant_service
