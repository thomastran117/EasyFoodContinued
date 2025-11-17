from typing import Literal
from service.authService import AuthService
from service.userService import UserService
from service.paymentService import PaymentService
from service.orderService import OrderService
from service.tokenService import TokenService
from service.oauthService import OAuthService
from service.webService import WebService
from service.categoryService import CategoryService
from service.restaurantService import RestaurantService
from service.bookingService import BookingService
from service.comboService import ComboService
from service.deliveryService import DeliveryService
from service.driverService import DriverService
from service.discountService import DiscountService
from service.drinkService import DrinkService
from service.employeeService import EmployeeService
from service.favouriteService import FavouriteService
from service.foodService import FoodService
from service.reservationService import ReservationService
from service.reviewService import ReviewService

Lifetime = Literal["singleton", "transient", "scoped"]


def register_services(
    container,
    *,
    auth_service_lifetime: Lifetime = "transient",
    oauth_service_lifetime: Lifetime = "transient",
    user_service_lifetime: Lifetime = "transient",
    payment_service_lifetime: Lifetime = "transient",
    token_service_lifetime: Lifetime = "transient",
    order_service_lifetime: Lifetime = "transient",
    web_service_lifetime: Lifetime = "transient",
    category_service_lifetime: Lifetime = "transient",
    restaurant_service_lifetime: Lifetime = "transient",
    booking_service_lifetime: Lifetime = "transient",
    combo_service_lifetime: Lifetime = "transient",
    delivery_service_lifetime: Lifetime = "transient",
    discount_service_lifetime: Lifetime = "transient",
    drink_service_lifetime: Lifetime = "transient",
    driver_service_lifetime: Lifetime = "transient",
    employee_service_lifetime: Lifetime = "transient",
    favourite_service_lifetime: Lifetime = "transient",
    food_service_lifetime: Lifetime = "transient",
    reservation_service_lifetime: Lifetime = "transient",
    review_service_lifetime: Lifetime = "transient",
):
    """Registers all app-level services."""

    container.register("OAuthService", lambda c: OAuthService(), oauth_service_lifetime)
    container.register("WebService", lambda c: WebService(), web_service_lifetime)

    async def token_factory(c):
        return TokenService(cache_service=await c.resolve("CacheService"))

    async def payment_factory(c):
        return PaymentService(web_service=await c.resolve("WebService"))

    async def user_factory(c):
        return UserService(file_service=await c.resolve("FileService"))

    async def order_factory(c):
        return OrderService(payment_service=await c.resolve("PaymentService"))

    async def category_factory(c):
        return CategoryService(cache_service=await c.resolve("CacheService"))

    async def delivery_factory(c):
        return DeliveryService(
            user_service=await c.resolve("UserService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def driver_factory(c):
        return DriverService(
            cache_service=await c.resolve("CacheService"),
        )

    async def restaurant_factory(c):
        return RestaurantService(
            user_service=await c.resolve("UserService"),
            category_service=await c.resolve("CategoryService"),
            cache_service=await c.resolve("CacheService"),
            file_service=await c.resolve("FileService"),
        )

    async def food_factory(c):
        return FoodService(
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def drink_factory(c):
        return DrinkService(
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def review_factory(c):
        return ReviewService(
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def reservation_factory(c):
        return ReservationService(
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def employee_factory(c):
        return EmployeeService(
            user_service=await c.resolve("UserService"),
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def favourite_factory(c):
        return FavouriteService(
            user_service=await c.resolve("UserService"),
            restaurant_service=await c.resolve("RestaurantService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def booking_factory(c):
        return BookingService(
            user_service=await c.resolve("UserService"),
            reservation_service=await c.resolve("ReservationService"),
            payment_service=await c.resolve("PaymentService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def combo_factory(c):
        return ComboService(
            food_service=await c.resolve("FoodService"),
            drink_service=await c.resolve("DrinkService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def discount_factory(c):
        return DiscountService(
            combo_service=await c.resolve("ComboService"),
            food_service=await c.resolve("FoodService"),
            drink_service=await c.resolve("DrinkService"),
            cache_service=await c.resolve("CacheService"),
        )

    async def auth_factory(c):
        return AuthService(
            token_service=await c.resolve("TokenService"),
            email_service=await c.resolve("EmailService"),
            oauth_service=await c.resolve("OAuthService"),
            web_service=await c.resolve("WebService"),
        )

    container.register("TokenService", token_factory, token_service_lifetime)
    container.register("PaymentService", payment_factory, payment_service_lifetime)
    container.register("UserService", user_factory, user_service_lifetime)
    container.register("OrderService", order_factory, order_service_lifetime)
    container.register("CategoryService", category_factory, category_service_lifetime)
    container.register(
        "RestaurantService", restaurant_factory, restaurant_service_lifetime
    )
    container.register("EmployeeService", employee_factory, employee_service_lifetime)
    container.register("DeliveryService", delivery_factory, delivery_service_lifetime)
    container.register("DriverService", driver_factory, driver_service_lifetime)
    container.register(
        "FavouriteService", favourite_factory, favourite_service_lifetime
    )
    container.register("ReviewService", review_factory, review_service_lifetime)
    container.register(
        "ReservationService", reservation_factory, reservation_service_lifetime
    )
    container.register("BookingService", booking_factory, booking_service_lifetime)
    container.register("AuthService", auth_factory, auth_service_lifetime)
    container.register("FoodService", food_factory, food_service_lifetime)
    container.register("DrinkService", drink_factory, drink_service_lifetime)
    container.register("ComboService", combo_factory, combo_service_lifetime)
    container.register("DiscountService", discount_factory, discount_service_lifetime)
    return container
