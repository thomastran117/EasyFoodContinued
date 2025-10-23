from fastapi import APIRouter

from controller.orderController import (
    createOrder,
    deleteOrder,
    getOrderById,
    getOrdersByRestaurant,
    getOrdersByUser,
    updateOrder,
)

orderRouter = APIRouter()
orderRouter.add_api_route("/restaurant", getOrdersByRestaurant, methods=["GET"])
orderRouter.add_api_route("/user", getOrdersByUser, methods=["GET"])
orderRouter.add_api_route("/{id}", getOrderById, methods=["GET"])
orderRouter.add_api_route("/", createOrder, methods=["POST"])
orderRouter.add_api_route("/{id}", updateOrder, methods=["PUT"])
orderRouter.add_api_route("/{id}", deleteOrder, methods=["DELETE"])
