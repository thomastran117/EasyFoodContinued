from fastapi import APIRouter
from controller.authController import (
    login,
    signup,
    verify_email,
    google_callback,
    google_login,
    microsoft_callback,
    microsoft_start,
)

authRouter = APIRouter()
authRouter.add_api_route("/login", login, methods=["POST"])
authRouter.add_api_route("/signup", signup, methods=["POST"])
authRouter.add_api_route("/verify", verify_email, methods=["GET"])
authRouter.add_api_route("/google/start", google_login, methods=["GET"])
authRouter.add_api_route("/google/callback", google_callback, methods=["GET"])
authRouter.add_api_route("/microsoft/start", microsoft_start, methods=["GET"])
authRouter.add_api_route("/microsoft/callback", microsoft_callback, methods=["GET"])
