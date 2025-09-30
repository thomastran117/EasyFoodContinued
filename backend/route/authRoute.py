from fastapi import APIRouter
from controller.authController import login, signup, verify_email

authRouter = APIRouter()
authRouter.add_api_route("/login", login, methods=["POST"])
authRouter.add_api_route("/signup", signup, methods=["POST"])
authRouter.add_api_route("/verify", verify_email, methods=["GET"])
