from datetime import datetime

from service.baseService import BaseService
from service.paymentService import PaymentService
from utilities.logger import logger


class OrderService:
    """
    Handles all order-related logic, including creating, retrieving,
    and cancelling orders, and delegating payments to PaymentService.
    """

    def __init__(self, payment_service: PaymentService):
        return
