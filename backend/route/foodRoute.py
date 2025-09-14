from fastapi import APIRouter
from controller.foodController import (
    getFood,
    getFoods,
    getFoodsByRestaurant,
    getFoodsByUserRestaurant,
    addFood,
    updateFood,
    deleteFood,
)

foodRouter = APIRouter()
foodRouter.add_api_route("/", getFoods, methods=["GET"])
foodRouter.add_api_route("/restaurant/user", getFoodsByUserRestaurant, methods=["GET"])
foodRouter.add_api_route("/restaurant/{id}", getFoodsByRestaurant, methods=["GET"])
foodRouter.add_api_route("/{id}", getFood, methods=["GET"])
foodRouter.add_api_route("/", addFood, methods=["POST"])
foodRouter.add_api_route("/{id}", updateFood, methods=["PUT"])
foodRouter.add_api_route("/{id}", deleteFood, methods=["DELETE"])
