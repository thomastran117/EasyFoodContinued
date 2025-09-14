from fastapi import APIRouter
from controller.reviewController import (
    getReviewById,
    getReviewsByRestaurant,
    getReviewsByUser,
    createReview,
    updateReview,
    deleteReview,
)

reviewRouter = APIRouter()
reviewRouter.add_api_route("/user", getReviewsByUser, methods=["GET"])
reviewRouter.add_api_route("/restaurant/{id}", getReviewsByRestaurant, methods=["GET"])
reviewRouter.add_api_route("/{id}", getReviewById, methods=["GET"])
reviewRouter.add_api_route("/{id}", createReview, methods=["POST"])
reviewRouter.add_api_route("/{id}", updateReview, methods=["PUT"])
reviewRouter.add_api_route("/{id}", deleteReview, methods=["DELETE"])
