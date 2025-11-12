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

    async def restaurant_factory(c):
        return RestaurantService(
            cache_service=await c.resolve("CacheService"),
            file_service=await c.resolve("FileService"),
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
    container.register("RestaurantService", restaurant_factory, restaurant_service_lifetime)
    container.register("AuthService", auth_factory, auth_service_lifetime)

    return container
