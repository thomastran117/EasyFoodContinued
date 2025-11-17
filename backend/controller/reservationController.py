from service.reservationService import ReservationService


class ReservationController:
    def __init__(self, reservation_service: ReservationService):
        self.reservation_service = reservation_service
