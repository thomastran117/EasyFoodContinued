from service.bookingService import BookingService


class BookingController:
    def __init__(self, booking_service: BookingService):
        self.booking_service = booking_service
