from utilities.logger import logger

from .container import Container
from .containerControllers import register_controllers
from .containerCore import init_connections
from .containerRepositories import register_repositories
from .containerServices import register_services


async def bootstrap() -> Container:
    try:
        logger.info("Bootstrapping IoC container asynchronously...")

        container = Container()
        await init_connections()
        register_repositories(container)
        register_services(
            container,
            default_lifetime="scoped",
            overrides={
                "CacheService": "singleton",
                "FileService": "singleton",
                "BasicTokenService": "singleton",
                "EmailService": "transient",
                "OAuthService": "transient",
                "WebService": "transient",
                "TokenService": "transient",
            },
        )
        register_controllers(container)

        await container.build()
        # container.summary()
        logger.info("IoC container Bootstrap completed.")
        return container
    except Exception as e:
        logger.error(f"[Container] Bootstrap failed: {e}")
        raise
