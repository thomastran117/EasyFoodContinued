from service.restaurantService import RestaurantService


class RestaurantController:
    def __init__(self, restaurantservice: RestaurantService):
        self.restaurant_service = restaurantservice
