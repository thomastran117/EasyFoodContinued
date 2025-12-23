from service.bookingService import BookingService


class BookingController:
    def __init__(self, bookingservice: BookingService):
        self.booking_service = bookingservice
