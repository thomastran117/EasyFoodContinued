from fastapi import HTTPException

from dtos.paymentDtos import PaymentCancelDto, PaymentCaptureDto, PaymentCreateDto
from service.paymentService import PaymentService
from utilities.logger import logger


class PaymentController:
    """
    Handles all payment-related endpoints (create, capture, cancel).
    """

    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service

    def create_payment(self, data: PaymentCreateDto):
        result = self.payment_service.create_payment(
            data.order_id, data.total, data.currency
        )
        if result["status"] != "created":
            raise HTTPException(status_code=400, detail=result)
        return result

    def capture_payment(self, token):
        result = self.payment_service.capture_payment(token)
        if result["status"] != "success":
            raise HTTPException(status_code=400, detail=result)
        return result

    def cancel_payment(self, data: PaymentCancelDto):
        result = self.payment_service.cancel_user_payment(data.paypal_order_id)
        if result["status"] != "cancelled":
            raise HTTPException(status_code=400, detail=result)
        return result

    def view_queue(self):
        return self.payment_service.view_queue()

    def clear_queue(self):
        return self.payment_service.clear_queue()
