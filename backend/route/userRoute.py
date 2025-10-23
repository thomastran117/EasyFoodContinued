from fastapi import APIRouter

from controller.userController import delete_me, get_me, get_user, update_me

userRouter = APIRouter()
userRouter.add_api_route("/", get_me, methods=["GET"])
userRouter.add_api_route("/{id}", get_user, methods=["GET"])
userRouter.add_api_route("/", update_me, methods=["PUT"])
userRouter.add_api_route("/", delete_me, methods=["DELETE"])
