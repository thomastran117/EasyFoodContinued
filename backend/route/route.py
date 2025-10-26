from fastapi import APIRouter

from route.authRoute import authRouter
from route.userRoute import userRouter

serverRouter = APIRouter()
serverRouter.include_router(authRouter, prefix="/auth")
serverRouter.include_router(userRouter, prefix="/users")
