from fastapi import Request
from dtos.paymentDtos import PaymentRequest
from service.paymentService import PaymentService


class PaymentController:
    def __init__(self, payment_service: PaymentService):
        """
        payment_service: instance of PaymentService (resolved by container)
        """
        self.payment_service = payment_service
        self.request: Request | None = None

    async def create_payment(self, dto: PaymentRequest):
        return self.payment_service.enqueue_payment(order_id="ORD-123", total=dto.total)

    async def cancel_payment(self, task_id: str):
        return self.payment_service.cancel_queued_payment(task_id)