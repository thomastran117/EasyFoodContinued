from fastapi import APIRouter, Depends, Request
from controller.paymentController import PaymentController
from dtos.paymentDtos import PaymentRequest, PaymentSuccessDto, PaymentCancelDto
from resources.container import container


def get_payment_controller(request: Request) -> PaymentController:
    """
    Resolve a new scoped PaymentController per request and
    automatically attach the FastAPI Request to it.
    """
    with container.create_scope() as scope:
        controller = container.resolve("PaymentController", scope)
        controller.request = request
        return controller


paymentRouter = APIRouter()


@paymentRouter.post("/queue")
async def queue_payment(dto: PaymentRequest, ctrl: PaymentController = Depends(get_payment_controller)):
    return await ctrl.create_payment(dto)

@paymentRouter.delete("/queue/{task_id}")
async def cancel_payment(task_id: str, ctrl: PaymentController = Depends(get_payment_controller)):
    return await ctrl.cancel_payment(task_id)