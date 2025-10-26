from fastapi import APIRouter

from controller.userController import UserController
from resources.container import class_container

userController: UserController = class_container.get_user_controller()

userRouter = APIRouter()
userRouter.add_api_route("/{id}", userController.get_user, methods=["GET"])
userRouter.add_api_route("/{id}", userController.update_user, methods=["PUT"])
userRouter.add_api_route("/{id}", userController.delete_user, methods=["DELETE"])
userRouter.add_api_route("/avatar", userController.update_avatar, methods=["POST"])
