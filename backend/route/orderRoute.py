from fastapi import APIRouter, Depends, Request
from controller.orderController import OrderController
from dtos.orderDtos import CreateOrderDto, CancelOrderDto
from container.containerEntry import container


def get_order_controller(request: Request) -> OrderController:
    """
    Resolve a new scoped AuthController per request and
    automatically attach the FastAPI Request to it.
    """
    with container.create_scope() as scope:
        controller = container.resolve("OrderController", scope)
        controller.request = request
        return controller


orderRouter = APIRouter()


@orderRouter.post("/")
async def create_order(
    dto: CreateOrderDto, ctrl: OrderController = Depends(get_order_controller)
):
    return await ctrl.create_order(dto)


@orderRouter.get("/{order_id}/status")
async def order_status(
    order_id: int, ctrl: OrderController = Depends(get_order_controller)
):
    return await ctrl.get_order_status(order_id)


@orderRouter.get("/user/{user_id}")
async def get_user_orders(
    user_id: int, ctrl: OrderController = Depends(get_order_controller)
):
    return await ctrl.get_user_orders(user_id)


@orderRouter.post("/cancel")
async def refresh(
    dto: CancelOrderDto, ctrl: OrderController = Depends(get_order_controller)
):
    return await ctrl.cancel_order(dto)
