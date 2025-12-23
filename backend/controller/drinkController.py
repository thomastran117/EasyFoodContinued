from service.drinkService import DrinkService


class DrinkController:
    def __init__(self, drinkservice: DrinkService):
        self.drink_service = drinkservice
