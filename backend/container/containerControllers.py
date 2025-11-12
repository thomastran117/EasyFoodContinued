from typing import Literal
from controller.authController import AuthController
from controller.userController import UserController
from controller.fileController import FileController
from controller.paymentController import PaymentController
from controller.orderController import OrderController
from controller.categoryController import CategoryController
from controller.restaurantController import RestaurantController

Lifetime = Literal["singleton", "transient", "scoped"]


def register_controllers(
    container,
    *,
    auth_controller_lifetime: Lifetime = "scoped",
    user_controller_lifetime: Lifetime = "scoped",
    file_controller_lifetime: Lifetime = "scoped",
    payment_controller_lifetime: Lifetime = "scoped",
    order_controller_lifetime: Lifetime = "scoped",
    category_controller_lifetime: Lifetime = "scoped",
    restaurant_controller_lifetime: Lifetime = "scoped",
):
    """Registers all controllers."""
    container.register(
        "AuthController",
        lambda c: AuthController(auth_service=c.resolve("AuthService")),
        auth_controller_lifetime,
    )
    container.register(
        "UserController",
        lambda c: UserController(user_service=c.resolve("UserService")),
        user_controller_lifetime,
    )
    container.register(
        "FileController",
        lambda c: FileController(file_service=c.resolve("FileService")),
        file_controller_lifetime,
    )
    container.register(
        "PaymentController",
        lambda c: PaymentController(payment_service=c.resolve("PaymentService")),
        payment_controller_lifetime,
    )
    container.register(
        "OrderController",
        lambda c: OrderController(order_service=c.resolve("OrderService")),
        order_controller_lifetime,
    )
    container.register(
        "CategoryController",
        lambda c: CategoryController(category_service=c.resolve("CategoryService")),
        category_controller_lifetime,
    )
    container.register(
        "RestaurantController",
        lambda c: RestaurantController(restaurant_service=c.resolve("RestaurantService")),
        restaurant_controller_lifetime,
    )
    return container
