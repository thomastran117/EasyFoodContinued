from service.cacheService import CacheService
from service.userService import UserService
from service.reservationService import ReservationService
from service.paymentService import PaymentService


class BookingService:
    def __init__(
        self,
        user_service: UserService,
        reservation_service: ReservationService,
        payment_service: PaymentService,
        cache_service: CacheService,
        ttl_seconds: int = 300,
    ):
        self.user_service = user_service
        self.reservation_service = reservation_service
        self.payment_service = payment_service
        self.cache = cache_service
        self.ttl = ttl_seconds
