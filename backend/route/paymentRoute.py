from fastapi import APIRouter, Depends, Request
from controller.paymentController import PaymentController
from resources.container import container


def get_payment_contorller(request: Request) -> PaymentController:
    """
    Resolve a new scoped AuthController per request and
    automatically attach the FastAPI Request to it.
    """
    with container.create_scope() as scope:
        controller = container.resolve("PaymentController", scope)
        controller.request = request
        return controller


paymentRouter = APIRouter(tags=["Payment"])


@paymentRouter.get("/success")
def handle_payment_success(
    paymentId: str,
    PayerID: str,
    ctrl: PaymentController = Depends(get_payment_contorller),
):
    return ctrl.payment_success(paymentId, PayerID)


@paymentRouter.get("/cancel")
def handle_payment_cancel(ctrl: PaymentController = Depends(get_payment_contorller)):
    return ctrl.payment_cancel()
