from typing import Literal

from repository.categoryRepository import CatagoryRepository
from repository.restaurantRepository import RestaurantRepository
from repository.userRepository import UserRepository
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


def register_repositories(
    container,
    *,
    user_repository_lifetime: Lifetime = "singleton",
    category_repository_lifetime: Lifetime = "singleton",
    restaurant_repository_lifetime: Lifetime = "singleton",
):
    """Registers all app-level services."""
    try:
        container.register(
            "UserRepository", lambda c, s: UserRepository(), user_repository_lifetime
        )
        container.register(
            "CatagoryRepository",
            lambda c, s: CatagoryRepository(),
            category_repository_lifetime,
        )
        container.register(
            "RestaurantRepository",
            lambda c, s: RestaurantRepository(),
            restaurant_repository_lifetime,
        )
        return container
    except Exception as e:
        logger.error(f"[Container] Repositories registration failed: {e}")
        raise
