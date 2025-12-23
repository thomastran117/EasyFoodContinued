from service.deliveryService import DeliveryService


class DeliveryController:
    def __init__(self, deliveryservice: DeliveryService):
        self.delivery_service = deliveryservice
