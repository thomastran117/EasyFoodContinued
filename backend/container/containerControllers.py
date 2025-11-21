from typing import Literal

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
    booking_controller_lifetime: Lifetime = "scoped",
    combo_controller_lifetime: Lifetime = "scoped",
    delivery_controller_lifetime: Lifetime = "scoped",
    discount_controller_lifetime: Lifetime = "scoped",
    drink_controller_lifetime: Lifetime = "scoped",
    driver_controller_lifetime: Lifetime = "scoped",
    employee_controller_lifetime: Lifetime = "scoped",
    favourite_controller_lifetime: Lifetime = "scoped",
    food_controller_lifetime: Lifetime = "scoped",
    reservation_controller_lifetime: Lifetime = "scoped",
    review_controller_lifetime: Lifetime = "scoped",
):
    try:
        """Registers all controllers."""

        async def auth_controller_factory(c, s):
            return AuthController(auth_service=await c.resolve("AuthService", s))

        async def user_controller_factory(c, s):
            return UserController(user_service=await c.resolve("UserService", s))

        async def file_controller_factory(c, s):
            return FileController(file_service=await c.resolve("FileService", s))

        async def payment_controller_factory(c, s):
            return PaymentController(
                payment_service=await c.resolve("PaymentService", s)
            )

        async def order_controller_factory(c, s):
            return OrderController(order_service=await c.resolve("OrderService", s))

        async def category_controller_factory(c, s):
            return CategoryController(
                category_service=await c.resolve("CategoryService", s)
            )

        async def restaurant_controller_factory(c, s):
            return RestaurantController(
                restaurant_service=await c.resolve("RestaurantService", s)
            )

        async def booking_controller_factory(c, s):
            return BookingController(
                booking_service=await c.resolve("BookingService", s)
            )

        async def combo_controller_factory(c, s):
            return ComboControler(combo_service=await c.resolve("ComboService", s))

        async def delivery_controller_factory(c, s):
            return DeliveryController(
                delivery_service=await c.resolve("DeliveryService", s)
            )

        async def discount_controller_factory(c, s):
            return DiscountController(
                discount_service=await c.resolve("DiscountService", s)
            )

        async def drink_controller_factory(c):
            return DrinkController(drink_service=await c.resolve("DrinkService", s))

        async def employee_controller_factory(c, s):
            return EmployeeController(
                employee_service=await c.resolve("EmployeeService, s")
            )

        async def favourite_controller_factory(c, s):
            return FavouriteController(
                favourite_service=await c.resolve("FavouriteService", s)
            )

        async def food_controller_factory(c, s):
            return FoodController(food_service=await c.resolve("FoodService", s))

        async def reservation_controller_factory(c, s):
            return ReservationController(
                reservation_service=await c.resolve("ReservationService", s)
            )

        async def driver_controller_factory(c, s):
            return DriverController(driver_service=await c.resolve("DriverService", s))

        async def review_controller_factory(c, s):
            return ReviewController(review_service=await c.resolve("ReviewService", s))

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
            "CategoryController",
            category_controller_factory,
            category_controller_lifetime,
        )
        container.register(
            "RestaurantController",
            restaurant_controller_factory,
            restaurant_controller_lifetime,
        )
        container.register(
            "BookingController",
            booking_controller_factory,
            booking_controller_lifetime,
        )
        container.register(
            "ComboController",
            combo_controller_factory,
            combo_controller_lifetime,
        )
        container.register(
            "DeliveryController",
            delivery_controller_factory,
            delivery_controller_lifetime,
        )
        container.register(
            "DriverController",
            driver_controller_factory,
            driver_controller_lifetime,
        )
        container.register(
            "DiscountController",
            discount_controller_factory,
            discount_controller_lifetime,
        )
        container.register(
            "DrinkController",
            drink_controller_factory,
            drink_controller_lifetime,
        )
        container.register(
            "EmployeeController",
            employee_controller_factory,
            employee_controller_lifetime,
        )
        container.register(
            "FavouriteController",
            favourite_controller_factory,
            favourite_controller_lifetime,
        )
        container.register(
            "FoodController",
            food_controller_factory,
            food_controller_lifetime,
        )
        container.register(
            "ReservationController",
            reservation_controller_factory,
            reservation_controller_lifetime,
        )
        container.register(
            "ReviewController",
            review_controller_factory,
            review_controller_lifetime,
        )

        return container
    except Exception as e:
        logger.error(f"[Container] Controller registration failed: {e}")
        raise
