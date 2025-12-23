from typing import Literal, Type, TypedDict

from service.authService import AuthService
from service.basicTokenService import BasicTokenService
from service.bookingService import BookingService
from service.cacheService import CacheService
from service.categoryService import CategoryService
from service.comboService import ComboService
from service.deliveryService import DeliveryService
from service.discountService import DiscountService
from service.drinkService import DrinkService
from service.driverService import DriverService
from service.emailService import EmailService
from service.employeeService import EmployeeService
from service.favouriteService import FavouriteService
from service.fileService import FileService
from service.foodService import FoodService
from service.oauthService import OAuthService
from service.orderService import OrderService
from service.paymentService import PaymentService
from service.reservationService import ReservationService
from service.restaurantService import RestaurantService
from service.reviewService import ReviewService
from service.tokenService import TokenService
from service.userService import UserService
from service.webService import WebService
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


class ServiceSpec(TypedDict):
    cls: Type
    deps: dict[str, str]


SERVICES: dict[str, ServiceSpec] = {
    "CacheService": {
        "cls": CacheService,
        "deps": {},
    },
    "FileService": {
        "cls": FileService,
        "deps": {},
    },
    "BasicTokenService": {
        "cls": BasicTokenService,
        "deps": {},
    },
    "EmailService": {
        "cls": EmailService,
        "deps": {},
    },
    "OAuthService": {
        "cls": OAuthService,
        "deps": {},
    },
    "WebService": {
        "cls": WebService,
        "deps": {},
    },
    "TokenService": {
        "cls": TokenService,
        "deps": {
            "cache_service": "CacheService",
        },
    },
    "PaymentService": {
        "cls": PaymentService,
        "deps": {
            "web_service": "WebService",
        },
    },
    "UserService": {
        "cls": UserService,
        "deps": {
            "user_repository": "UserRepository",
            "file_service": "FileService",
        },
    },
    "OrderService": {
        "cls": OrderService,
        "deps": {
            "payment_service": "PaymentService",
        },
    },
    "CategoryService": {
        "cls": CategoryService,
        "deps": {
            "cache_service": "CacheService",
        },
    },
    "RestaurantService": {
        "cls": RestaurantService,
        "deps": {
            "user_service": "UserService",
            "category_service": "CategoryService",
            "cache_service": "CacheService",
            "file_service": "FileService",
        },
    },
    "FoodService": {
        "cls": FoodService,
        "deps": {
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "DrinkService": {
        "cls": DrinkService,
        "deps": {
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "ReviewService": {
        "cls": ReviewService,
        "deps": {
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "ReservationService": {
        "cls": ReservationService,
        "deps": {
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "EmployeeService": {
        "cls": EmployeeService,
        "deps": {
            "user_service": "UserService",
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "FavouriteService": {
        "cls": FavouriteService,
        "deps": {
            "user_service": "UserService",
            "restaurant_service": "RestaurantService",
            "cache_service": "CacheService",
        },
    },
    "DriverService": {
        "cls": DriverService,
        "deps": {
            "cache_service": "CacheService",
        },
    },
    "DeliveryService": {
        "cls": DeliveryService,
        "deps": {
            "user_service": "UserService",
            "cache_service": "CacheService",
        },
    },
    "BookingService": {
        "cls": BookingService,
        "deps": {
            "user_service": "UserService",
            "reservation_service": "ReservationService",
            "payment_service": "PaymentService",
            "cache_service": "CacheService",
        },
    },
    "ComboService": {
        "cls": ComboService,
        "deps": {
            "food_service": "FoodService",
            "drink_service": "DrinkService",
            "cache_service": "CacheService",
        },
    },
    "DiscountService": {
        "cls": DiscountService,
        "deps": {
            "combo_service": "ComboService",
            "food_service": "FoodService",
            "drink_service": "DrinkService",
            "cache_service": "CacheService",
        },
    },
    "AuthService": {
        "cls": AuthService,
        "deps": {
            "user_repository": "UserRepository",
            "token_service": "TokenService",
            "email_service": "EmailService",
            "oauth_service": "OAuthService",
            "web_service": "WebService",
        },
    },
}


def make_service_factory(cls, deps: dict[str, str]):
    async def factory(container, scope):
        resolved = {
            arg: await container.resolve(service_name, scope)
            for arg, service_name in deps.items()
        }
        return cls(**resolved)

    return factory


def register_services(
    container,
    *,
    default_lifetime: Lifetime = "scoped",
    overrides: dict[str, Lifetime] | None = None,
):
    """
    Registers all services using a declarative registry.

    overrides example:
        {
            "CacheService": "singleton",
            "EmailService": "transient",
            "TokenService": "singleton",
        }
    """
    overrides = overrides or {}

    try:
        for name, spec in SERVICES.items():
            lifetime = overrides.get(name, default_lifetime)

            container.register(
                name,
                make_service_factory(spec["cls"], spec["deps"]),
                lifetime,
            )

        logger.info("[Container] Services registered successfully")
        return container

    except Exception as e:
        logger.error(f"[Container] Services registration failed: {e}")
        raise
