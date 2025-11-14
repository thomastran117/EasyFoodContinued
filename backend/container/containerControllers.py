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

    async def auth_controller_factory(c):
        return AuthController(auth_service=await c.resolve("AuthService"))

    async def user_controller_factory(c):
        return UserController(user_service=await c.resolve("UserService"))

    async def file_controller_factory(c):
        return FileController(file_service=await c.resolve("FileService"))

    async def payment_controller_factory(c):
        return PaymentController(payment_service=await c.resolve("PaymentService"))

    async def order_controller_factory(c):
        return OrderController(order_service=await c.resolve("OrderService"))

    async def category_controller_factory(c):
        return CategoryController(category_service=await c.resolve("CategoryService"))

    async def restaurant_controller_factory(c):
        return RestaurantController(
            restaurant_service=await c.resolve("RestaurantService")
        )

    container.register(
        "AuthController", auth_controller_factory, auth_controller_lifetime
    )
    container.register(
        "UserController", user_controller_factory, user_controller_lifetime
    )
    container.register(
        "FileController", file_controller_factory, file_controller_lifetime
    )
    container.register(
        "PaymentController", payment_controller_factory, payment_controller_lifetime
    )
    container.register(
        "OrderController", order_controller_factory, order_controller_lifetime
    )
    container.register(
        "CategoryController", category_controller_factory, category_controller_lifetime
    )
    container.register(
        "RestaurantController",
        restaurant_controller_factory,
        restaurant_controller_lifetime,
    )

    return container
