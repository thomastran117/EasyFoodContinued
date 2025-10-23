from fastapi import APIRouter

from route.authRoute import authRouter
from route.foodRoute import foodRouter
from route.orderRoute import orderRouter
from route.reservationRoute import reservationRouter
from route.restaurantRoute import restaurantRouter
from route.reviewRoute import reviewRouter
from route.surveyRoute import surveyRouter
from route.userRoute import userRouter

serverRouter = APIRouter()
serverRouter.include_router(authRouter, prefix="/auth")
# serverRouter.include_router(userRouter, prefix="/user")
# serverRouter.include_router(restaurantRouter, prefix="/restaurant")
# serverRouter.include_router(foodRouter, prefix="/food")
# app.include_router(reviewRouter, prefix="/review")
# app.include_router(reservationRouter, prefix="/reservation")
# serverRouter.include_router(surveyRouter, prefix="/survey")
# serverRouter.include_router(orderRouter, prefix="/order")
