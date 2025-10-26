from fastapi import APIRouter

from route.authRoute import authRouter
from route.userRoute import userRouter
from route.fileRoute import fileRouter

serverRouter = APIRouter()
serverRouter.include_router(authRouter, prefix="/auth")
serverRouter.include_router(userRouter, prefix="/users")
serverRouter.include_router(fileRouter, prefix="/files")
