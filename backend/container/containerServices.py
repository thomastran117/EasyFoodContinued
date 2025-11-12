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
    container.register(
        "OAuthService",
        lambda c: OAuthService(),
        oauth_service_lifetime,
    )
    container.register(
        "WebService",
        lambda c: WebService(),
        web_service_lifetime,
    )
    container.register(
        "TokenService",
        lambda c: TokenService(cache_service=c.resolve("CacheService")),
        token_service_lifetime,
    )
    container.register(
        "PaymentService",
        lambda c: PaymentService(web_service=c.resolve("WebService")),
        payment_service_lifetime,
    )
    container.register(
        "UserService",
        lambda c: UserService(file_service=c.resolve("FileService")),
        user_service_lifetime,
    )
    container.register(
        "OrderService",
        lambda c: OrderService(payment_service=c.resolve("PaymentService")),
        order_service_lifetime,
    )
    container.register(
        "CategoryService",
        lambda c: CategoryService(cache_service=c.resolve("CacheService")),
        category_service_lifetime,
    )
    container.register(
        "RestaurantService",
        lambda c: RestaurantService(
            cache_service=c.resolve("CacheService"),
            file_service=c.resolve("FileService"),
        ),
        restaurant_service_lifetime,
    )
    container.register(
        "AuthService",
        lambda c: AuthService(
            token_service=c.resolve("TokenService"),
            email_service=c.resolve("EmailService"),
            oauth_service=c.resolve("OAuthService"),
        ),
        auth_service_lifetime,
    )
    return container
