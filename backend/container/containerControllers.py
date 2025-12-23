from typing import Literal, Type, TypedDict

from controller.authController import AuthController
from controller.bookingController import BookingController
from controller.categoryController import CategoryController
from controller.comboController import ComboControler
from controller.deliveryController import DeliveryController
from controller.discountController import DiscountController
from controller.drinkController import DrinkController
from controller.driverController import DriverController
from controller.employeeController import EmployeeController
from controller.favouriteController import FavouriteController
from controller.fileController import FileController
from controller.foodController import FoodController
from controller.orderController import OrderController
from controller.paymentController import PaymentController
from controller.reservationController import ReservationController
from controller.restaurantController import RestaurantController
from controller.reviewController import ReviewController
from controller.userController import UserController
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


class ControllerSpec(TypedDict):
    controller: Type
    service: str


CONTROLLERS: dict[str, ControllerSpec] = {
    "AuthController": {
        "controller": AuthController,
        "service": "AuthService",
    },
    "UserController": {
        "controller": UserController,
        "service": "UserService",
    },
    "FileController": {
        "controller": FileController,
        "service": "FileService",
    },
    "PaymentController": {
        "controller": PaymentController,
        "service": "PaymentService",
    },
    "OrderController": {
        "controller": OrderController,
        "service": "OrderService",
    },
    "CategoryController": {
        "controller": CategoryController,
        "service": "CategoryService",
    },
    "RestaurantController": {
        "controller": RestaurantController,
        "service": "RestaurantService",
    },
    "BookingController": {
        "controller": BookingController,
        "service": "BookingService",
    },
    "ComboController": {
        "controller": ComboControler,
        "service": "ComboService",
    },
    "DeliveryController": {
        "controller": DeliveryController,
        "service": "DeliveryService",
    },
    "DiscountController": {
        "controller": DiscountController,
        "service": "DiscountService",
    },
    "DrinkController": {
        "controller": DrinkController,
        "service": "DrinkService",
    },
    "EmployeeController": {
        "controller": EmployeeController,
        "service": "EmployeeService",
    },
    "FavouriteController": {
        "controller": FavouriteController,
        "service": "FavouriteService",
    },
    "FoodController": {
        "controller": FoodController,
        "service": "FoodService",
    },
    "ReservationController": {
        "controller": ReservationController,
        "service": "ReservationService",
    },
    "DriverController": {
        "controller": DriverController,
        "service": "DriverService",
    },
    "ReviewController": {
        "controller": ReviewController,
        "service": "ReviewService",
    },
}


def make_controller_factory(controller_cls, service_name: str):
    async def factory(container, scope):
        service = await container.resolve(service_name, scope)
        return controller_cls(**{service_name.lower(): service})

    return factory


def register_controllers(
    container,
    *,
    default_lifetime: Lifetime = "scoped",
    overrides: dict[str, Lifetime] | None = None,
):
    """
    Registers all controllers using a generic factory.

    overrides:
        {
            "AuthController": "singleton",
            "FileController": "transient"
        }
    """
    overrides = overrides or {}

    try:
        for name, spec in CONTROLLERS.items():
            lifetime = overrides.get(name, default_lifetime)

            container.register(
                name,
                make_controller_factory(
                    spec["controller"],
                    spec["service"],
                ),
                lifetime,
            )

        logger.info("[Container] Controllers registered successfully")
        return container

    except Exception as e:
        logger.error(f"[Container] Controller registration failed: {e}")
        raise
