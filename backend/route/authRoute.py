from fastapi import APIRouter
from controller.authController import AuthController
from resources.container import class_container

authController: AuthController = class_container.get_auth_controller()

authRouter = APIRouter()
authRouter.add_api_route("/login", authController.login, methods=["POST"])
authRouter.add_api_route("/signup", authController.signup, methods=["POST"])
authRouter.add_api_route("/verify", authController.verify_email, methods=["GET"])
authRouter.add_api_route("/refresh", authController.renew, methods=["POST"])
authRouter.add_api_route("/logout", authController.logout, methods=["POST"])
authRouter.add_api_route("/google", authController.google, methods=["POST"])
authRouter.add_api_route("/microsoft", authController.microsoft, methods=["POST"])
authRouter.add_api_route(
    "/forgot-password", authController.forgot_password, methods=["POST"]
)
authRouter.add_api_route(
    "/change-password", authController.change_password, methods=["POST"]
)
