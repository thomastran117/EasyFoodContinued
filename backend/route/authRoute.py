from fastapi import APIRouter
from controller.authController import (
    login,
    signup,
    verify_email,
    renew,
    logout,
    google,
    microsoft,
)

authRouter = APIRouter()
authRouter.add_api_route("/login", login, methods=["POST"])
authRouter.add_api_route("/signup", signup, methods=["POST"])
authRouter.add_api_route("/verify", verify_email, methods=["GET"])
authRouter.add_api_route("/refresh", renew, methods=["POST"])
authRouter.add_api_route("/logout", logout, methods=["POST"])
authRouter.add_api_route("/google", google, methods=["POST"])
authRouter.add_api_route("/microsoft", microsoft, methods=["POST"])
