from fastapi import APIRouter
from controller.authController import AuthController

class AuthRoutes:
    def __init__(self, auth_controller: AuthController):
        self.auth_controller = auth_controller
        self.authRouter = APIRouter()
        self.authRouter.add_api_route("/login", self.auth_controller.login, methods=["POST"])
        self.authRouter.add_api_route("/signup", self.auth_controller.signup, methods=["POST"])
        self.authRouter.add_api_route("/verify", self.auth_controller.verify_email, methods=["GET"])
        self.authRouter.add_api_route("/refresh", self.auth_controller.renew, methods=["POST"])
        self.authRouter.add_api_route("/logout", self.auth_controller.logout, methods=["POST"])
        self.authRouter.add_api_route("/google", self.auth_controller.google, methods=["POST"])
        self.authRouter.add_api_route("/microsoft", self.auth_controller.microsoft, methods=["POST"])
        self.authRouter.add_api_route("/forgot-password", self.auth_controller.forgot_password, methods=["POST"])
        self.authRouter.add_api_route("/change-password", self.auth_controller.change_password, methods=["POST"])
