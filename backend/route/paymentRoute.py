from fastapi import APIRouter, Depends, Request
from controller.paymentController import PaymentController
from dtos.paymentDtos import (
    PaymentCreateDto,
    PaymentCaptureDto,
    PaymentCancelDto,
)
from resources.container import container


def get_payment_controller(request: Request) -> PaymentController:
    """
    Resolve a new scoped PaymentController per request.
    """
    with container.create_scope() as scope:
        controller = container.resolve("PaymentController", scope)
        controller.request = request
        return controller


paymentRouter = APIRouter(tags=["Payment"])


@paymentRouter.post("/create", summary="Create a PayPal order")
def create_payment(
    body: PaymentCreateDto,
    ctrl: PaymentController = Depends(get_payment_controller),
):
    """
    Creates a PayPal order and schedules the auto-finalization pipeline.
    Returns the approval URL for the client to redirect to PayPal.
    """
    return ctrl.create_payment(body)


@paymentRouter.get("/capture", summary="Capture a PayPal order after approval")
def capture_payment(
    token: str,
    ctrl: PaymentController = Depends(get_payment_controller),
):
    """
    Called by PayPal (or frontend redirect) after user approves the payment.
    The `token` query parameter is the PayPal order ID.
    Captures and marks the order as paid, revoking any scheduled cancel jobs.
    """
    return ctrl.capture_payment(token)


@paymentRouter.post("/cancel", summary="Cancel a PayPal order manually")
def cancel_payment(
    body: PaymentCancelDto,
    ctrl: PaymentController = Depends(get_payment_controller),
):
    """
    Called when user cancels payment before approval.
    Voids the PayPal order and marks it as cancelled in DB.
    """
    return ctrl.cancel_payment(body)


@paymentRouter.get("/queue", summary="View Celery queue state")
def view_queue(ctrl: PaymentController = Depends(get_payment_controller)):
    """
    Returns active, reserved, scheduled, and revoked tasks.
    """
    return ctrl.view_queue()


@paymentRouter.delete("/queue", summary="Clear all Celery queues")
def clear_queue(ctrl: PaymentController = Depends(get_payment_controller)):
    """
    Purges all queued Celery tasks.
    Use with caution.
    """
    return ctrl.clear_queue()
