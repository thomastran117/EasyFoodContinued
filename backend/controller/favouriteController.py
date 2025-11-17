from service.favouriteService import FavouriteService


class FavouriteController:
    def __init__(self, favourite_service: FavouriteService):
        self.favourite_service = favourite_service
