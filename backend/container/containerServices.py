from typing import Literal

from service.authService import AuthService
from service.basicTokenService import BasicTokenService
from service.bookingService import BookingService
from service.cacheService import CacheService
from service.categoryService import CategoryService
from service.comboService import ComboService
from service.deliveryService import DeliveryService
from service.discountService import DiscountService
from service.drinkService import DrinkService
from service.driverService import DriverService
from service.emailService import EmailService
from service.employeeService import EmployeeService
from service.favouriteService import FavouriteService
from service.fileService import FileService
from service.foodService import FoodService
from service.oauthService import OAuthService
from service.orderService import OrderService
from service.paymentService import PaymentService
from service.reservationService import ReservationService
from service.restaurantService import RestaurantService
from service.reviewService import ReviewService
from service.tokenService import TokenService
from service.userService import UserService
from service.webService import WebService
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


def register_services(
    container,
    *,
    cache_lifetime: Lifetime = "singleton",
    file_lifetime: Lifetime = "singleton",
    basic_token_service_lifetime: Lifetime = "singleton",
    auth_service_lifetime: Lifetime = "scoped",
    email_lifetime: Lifetime = "transient",
    oauth_service_lifetime: Lifetime = "transient",
    user_service_lifetime: Lifetime = "scoped",
    payment_service_lifetime: Lifetime = "scoped",
    token_service_lifetime: Lifetime = "transient",
    order_service_lifetime: Lifetime = "scoped",
    web_service_lifetime: Lifetime = "transient",
    category_service_lifetime: Lifetime = "scoped",
    restaurant_service_lifetime: Lifetime = "scoped",
    booking_service_lifetime: Lifetime = "scoped",
    combo_service_lifetime: Lifetime = "scoped",
    delivery_service_lifetime: Lifetime = "scoped",
    discount_service_lifetime: Lifetime = "scoped",
    drink_service_lifetime: Lifetime = "scoped",
    driver_service_lifetime: Lifetime = "scoped",
    employee_service_lifetime: Lifetime = "scoped",
    favourite_service_lifetime: Lifetime = "scoped",
    food_service_lifetime: Lifetime = "scoped",
    reservation_service_lifetime: Lifetime = "scoped",
    review_service_lifetime: Lifetime = "scoped",
):
    """Registers all app-level services."""
    try:

        async def token_factory(c, s):
            return TokenService(cache_service=await c.resolve("CacheService", s))

        async def payment_factory(c, s):
            return PaymentService(web_service=await c.resolve("WebService", s))

        async def user_factory(c, s):
            return UserService(
                user_repository=await c.resolve("UserRepository", s),
                file_service=await c.resolve("FileService", s),
            )

        async def order_factory(c, s):
            return OrderService(payment_service=await c.resolve("PaymentService", s))

        async def category_factory(c, s):
            return CategoryService(cache_service=await c.resolve("CacheService", s))

        async def delivery_factory(c, s):
            return DeliveryService(
                user_service=await c.resolve("UserService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def driver_factory(c, s):
            return DriverService(
                cache_service=await c.resolve("CacheService", s),
            )

        async def restaurant_factory(c, s):
            return RestaurantService(
                user_service=await c.resolve("UserService", s),
                category_service=await c.resolve("CategoryService", s),
                cache_service=await c.resolve("CacheService", s),
                file_service=await c.resolve("FileService", s),
            )

        async def food_factory(c, s):
            return FoodService(
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def drink_factory(c, s):
            return DrinkService(
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def review_factory(c, s):
            return ReviewService(
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def reservation_factory(c, s):
            return ReservationService(
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def employee_factory(c, s):
            return EmployeeService(
                user_service=await c.resolve("UserService", s),
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def favourite_factory(c, s):
            return FavouriteService(
                user_service=await c.resolve("UserService", s),
                restaurant_service=await c.resolve("RestaurantService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def booking_factory(c, s):
            return BookingService(
                user_service=await c.resolve("UserService", s),
                reservation_service=await c.resolve("ReservationService", s),
                payment_service=await c.resolve("PaymentService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def combo_factory(c, s):
            return ComboService(
                food_service=await c.resolve("FoodService", s),
                drink_service=await c.resolve("DrinkService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def discount_factory(c, s):
            return DiscountService(
                combo_service=await c.resolve("ComboService", s),
                food_service=await c.resolve("FoodService", s),
                drink_service=await c.resolve("DrinkService", s),
                cache_service=await c.resolve("CacheService", s),
            )

        async def auth_factory(c, s):
            return AuthService(
                user_repository=await c.resolve("UserRepository", s),
                token_service=await c.resolve("TokenService", s),
                email_service=await c.resolve("EmailService", s),
                oauth_service=await c.resolve("OAuthService", s),
                web_service=await c.resolve("WebService", s),
            )

        container.register("CacheService", lambda c, s: CacheService(), cache_lifetime)
        container.register("FileService", lambda c, s: FileService(), file_lifetime)
        container.register(
            "BasicTokenService",
            lambda c, s: BasicTokenService(),
            basic_token_service_lifetime,
        )
        container.register("EmailService", lambda c, s: EmailService(), email_lifetime)
        container.register(
            "OAuthService", lambda c, s: OAuthService(), oauth_service_lifetime
        )
        container.register(
            "WebService", lambda c, s: WebService(), web_service_lifetime
        )

        container.register("TokenService", token_factory, token_service_lifetime)
        container.register("PaymentService", payment_factory, payment_service_lifetime)
        container.register("UserService", user_factory, user_service_lifetime)
        container.register("OrderService", order_factory, order_service_lifetime)
        container.register(
            "CategoryService", category_factory, category_service_lifetime
        )
        container.register(
            "RestaurantService", restaurant_factory, restaurant_service_lifetime
        )
        container.register(
            "EmployeeService", employee_factory, employee_service_lifetime
        )
        container.register(
            "DeliveryService", delivery_factory, delivery_service_lifetime
        )
        container.register("DriverService", driver_factory, driver_service_lifetime)
        container.register(
            "FavouriteService", favourite_factory, favourite_service_lifetime
        )
        container.register("ReviewService", review_factory, review_service_lifetime)
        container.register(
            "ReservationService", reservation_factory, reservation_service_lifetime
        )
        container.register("BookingService", booking_factory, booking_service_lifetime)
        container.register("FoodService", food_factory, food_service_lifetime)
        container.register("DrinkService", drink_factory, drink_service_lifetime)
        container.register("ComboService", combo_factory, combo_service_lifetime)
        container.register(
            "DiscountService", discount_factory, discount_service_lifetime
        )
        container.register("AuthService", auth_factory, auth_service_lifetime)
        return container
    except Exception as e:
        logger.error(f"[Container] Services registration failed: {e}")
        raise
