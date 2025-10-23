from fastapi import APIRouter

from controller.restaurantController import (
    addRestaurant,
    deleteRestaurant,
    getRestaurant,
    getRestaurants,
    getUserRestaurant,
    updateRestaurant,
)

restaurantRouter = APIRouter()
restaurantRouter.add_api_route("/", getRestaurants, methods=["GET"])
restaurantRouter.add_api_route("/user", getUserRestaurant, methods=["GET"])
restaurantRouter.add_api_route("/{id}", getRestaurant, methods=["GET"])
restaurantRouter.add_api_route("/", addRestaurant, methods=["POST"])
restaurantRouter.add_api_route("/", updateRestaurant, methods=["PUT"])
restaurantRouter.add_api_route("/", deleteRestaurant, methods=["DELETE"])
