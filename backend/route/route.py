from fastapi import APIRouter

from route.authRoute import authRouter
from route.userRoute import userRouter
from route.fileRoute import fileRouter
from route.paymentRoute import paymentRouter
from route.orderRoute import orderRouter
from route.categoryRoute import categoryRouter

serverRouter = APIRouter()
serverRouter.include_router(authRouter, prefix="/auth")
serverRouter.include_router(userRouter, prefix="/users")
serverRouter.include_router(fileRouter, prefix="/files")
serverRouter.include_router(orderRouter, prefix="/orders")
serverRouter.include_router(paymentRouter, prefix="/payment")
serverRouter.include_router(categoryRouter, prefix="/categories")
