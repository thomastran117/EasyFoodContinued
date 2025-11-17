from service.drinkService import DrinkService


class DrinkController:
    def __init__(self, drink_service: DrinkService):
        self.drink_service = drink_service
