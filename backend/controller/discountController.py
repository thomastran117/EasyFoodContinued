from service.discountService import DiscountService


class DiscountController:
    def __init__(self, discountservice: DiscountService):
        self.discount_service = discountservice
