from service.favouriteService import FavouriteService


class FavouriteController:
    def __init__(self, favouriteservice: FavouriteService):
        self.favourite_service = favouriteservice
