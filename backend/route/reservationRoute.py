from fastapi import APIRouter
from controller.reservationController import (
    getReservationsByRestaurant,
    getReservationsByUser,
    getReservationById,
    createReservation,
    updateReservation,
    deleteReservation,
)

reservationRouter = APIRouter()
reservationRouter.add_api_route("/user", getReservationsByUser, methods=["GET"])
reservationRouter.add_api_route(
    "/restaurant/{id}", getReservationsByRestaurant, methods=["GET"]
)
reservationRouter.add_api_route("/{id}", getReservationById, methods=["GET"])
reservationRouter.add_api_route("/{id}", createReservation, methods=["POST"])
reservationRouter.add_api_route("/{id}", updateReservation, methods=["PUT"])
reservationRouter.add_api_route("/{id}", deleteReservation, methods=["DELETE"])
