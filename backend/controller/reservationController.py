from service.reservationService import ReservationService


class ReservationController:
    def __init__(self, reservationservice: ReservationService):
        self.reservation_service = reservationservice
