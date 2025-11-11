from typing import Literal
from controller.authController import AuthController
from controller.userController import UserController
from controller.fileController import FileController
from controller.paymentController import PaymentController
from controller.orderController import OrderController

Lifetime = Literal["singleton", "transient", "scoped"]


def register_controllers(
    container,
    *,
    auth_controller_lifetime: Lifetime = "scoped",
    user_controller_lifetime: Lifetime = "scoped",
    file_controller_lifetime: Lifetime = "scoped",
    payment_controller_lifetime: Lifetime = "scoped",
    order_controller_lifetime: Lifetime = "scoped",
):
    """Registers all controllers."""
    container.register(
        "AuthController",
        lambda c: AuthController(c.resolve("AuthService")),
        auth_controller_lifetime,
    )
    container.register(
        "UserController",
        lambda c: UserController(c.resolve("UserService")),
        user_controller_lifetime,
    )
    container.register(
        "FileController",
        lambda c: FileController(c.resolve("FileService")),
        file_controller_lifetime,
    )
    container.register(
        "PaymentController",
        lambda c: PaymentController(c.resolve("PaymentService")),
        payment_controller_lifetime,
    )
    container.register(
        "OrderController",
        lambda c: OrderController(c.resolve("OrderService")),
        order_controller_lifetime,
    )
    return container
