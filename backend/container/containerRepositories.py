from typing import Literal, Type, TypedDict

from repository.categoryRepository import CatagoryRepository
from repository.restaurantRepository import RestaurantRepository
from repository.userRepository import UserRepository
from utilities.logger import logger

Lifetime = Literal["singleton", "transient", "scoped"]


class RepositorySpec(TypedDict):
    cls: Type


REPOSITORIES: dict[str, RepositorySpec] = {
    "UserRepository": {
        "cls": UserRepository,
    },
    "CategoryRepository": {
        "cls": CatagoryRepository,
    },
    "RestaurantRepository": {
        "cls": RestaurantRepository,
    },
}


def make_repository_factory(cls):
    async def factory(container, scope):
        return cls()

    return factory


def register_repositories(
    container,
    *,
    default_lifetime: Lifetime = "singleton",
    overrides: dict[str, Lifetime] | None = None,
):
    """
    Registers all repositories.

    overrides example:
        {
            "UserRepository": "scoped"
        }
    """
    overrides = overrides or {}

    try:
        for name, spec in REPOSITORIES.items():
            lifetime = overrides.get(name, default_lifetime)

            container.register(
                name,
                make_repository_factory(spec["cls"]),
                lifetime,
            )

        logger.info("[Container] Repositories registered successfully")
        return container

    except Exception as e:
        logger.error(f"[Container] Repositories registration failed: {e}")
        raise
