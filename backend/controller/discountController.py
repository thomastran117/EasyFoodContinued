from service.discountService import DiscountService


class DiscountController:
    def __init__(self, discount_service: DiscountService):
        self.discount_service = discount_service
