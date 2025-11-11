from typing import Literal
from service.authService import AuthService
from service.userService import UserService
from service.paymentService import PaymentService
from service.orderService import OrderService
from service.tokenService import TokenService

Lifetime = Literal["singleton", "transient", "scoped"]


def register_services(
    container,
    *,
    auth_service_lifetime: Lifetime = "transient",
    user_service_lifetime: Lifetime = "transient",
    payment_service_lifetime: Lifetime = "transient",
    token_service_lifetime: Lifetime = "transient",
    order_service_lifetime: Lifetime = "transient",
):
    """Registers all app-level services."""
    container.register(
        "TokenService",
        lambda c: TokenService(c.resolve("CacheService")),
        token_service_lifetime,
    )
    container.register(
        "AuthService",
        lambda c: AuthService(
            token_service=c.resolve("TokenService"),
            email_service=c.resolve("EmailService"),
        ),
        auth_service_lifetime,
    )
    container.register(
        "UserService",
        lambda c: UserService(c.resolve("FileService")),
        user_service_lifetime,
    )
    container.register(
        "PaymentService",
        lambda c: PaymentService(),
        payment_service_lifetime,
    )
    container.register(
        "OrderService",
        lambda c: OrderService(c.resolve("PaymentService")),
        order_service_lifetime,
    )
    return container
