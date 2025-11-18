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

    async def booking_controller_factory(c):
        return BookingController(booking_service=await c.resolve("BookingService"))

    async def combo_controller_factory(c):
        return ComboControler(combo_service=await c.resolve("ComboService"))

    async def delivery_controller_factory(c):
        return DeliveryController(delivery_service=await c.resolve("DeliveryService"))

    async def discount_controller_factory(c):
        return DiscountController(discount_service=await c.resolve("DiscountService"))

    async def drink_controller_factory(c):
        return DrinkController(drink_service=await c.resolve("DrinkService"))

    async def employee_controller_factory(c):
        return EmployeeController(employee_service=await c.resolve("EmployeeService"))

    async def favourite_controller_factory(c):
        return FavouriteController(
            favourite_service=await c.resolve("FavouriteService")
        )

    async def food_controller_factory(c):
        return FoodController(food_service=await c.resolve("FoodService"))

    async def reservation_controller_factory(c):
        return ReservationController(
            reservation_service=await c.resolve("ReservationService")
        )

    async def driver_controller_factory(c):
        return DriverController(driver_service=await c.resolve("DriverService"))

    async def review_controller_factory(c):
        return ReviewController(review_service=await c.resolve("ReviewService"))

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
