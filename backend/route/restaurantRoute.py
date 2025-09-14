from fastapi import APIRouter
from controller.restaurantController import (
    getRestaurant,
    getRestaurants,
    getUserRestaurant,
    addRestaurant,
    updateRestaurant,
    deleteRestaurant,
)

restaurantRouter = APIRouter()
restaurantRouter.add_api_route("/", getRestaurants, methods=["GET"])
restaurantRouter.add_api_route("/user", getUserRestaurant, methods=["GET"])
restaurantRouter.add_api_route("/{id}", getRestaurant, methods=["GET"])
restaurantRouter.add_api_route("/", addRestaurant, methods=["POST"])
restaurantRouter.add_api_route("/", updateRestaurant, methods=["PUT"])
restaurantRouter.add_api_route("/", deleteRestaurant, methods=["DELETE"])
