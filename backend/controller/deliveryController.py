from service.deliveryService import DeliveryService


class DeliveryController:
    def __init__(self, delivery_service: DeliveryService):
        self.delivery_service = delivery_service
