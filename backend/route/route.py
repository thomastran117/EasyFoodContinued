from fastapi import APIRouter

from route.authRoute import authRouter
from route.userRoute import userRouter
from route.restaurantRoute import restaurantRouter
from route.foodRoute import foodRouter
from route.reservationRoute import reservationRouter
from route.reviewRoute import reviewRouter
from route.orderRoute import orderRouter
from route.surveyRoute import surveyRouter

serverRouter = APIRouter()
serverRouter.include_router(authRouter, prefix="/auth")
# serverRouter.include_router(userRouter, prefix="/user")
# serverRouter.include_router(restaurantRouter, prefix="/restaurant")
# serverRouter.include_router(foodRouter, prefix="/food")
# app.include_router(reviewRouter, prefix="/review")
# app.include_router(reservationRouter, prefix="/reservation")
# serverRouter.include_router(surveyRouter, prefix="/survey")
# serverRouter.include_router(orderRouter, prefix="/order")
