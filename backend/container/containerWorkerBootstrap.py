import asyncio

from container.container import Container
from container.containerControllers import register_controllers
from container.containerCore import register_singletons
from container.containerServices import register_services
from utilities.logger import logger


async def async_bootstrap_worker() -> Container:
    """
    Asynchronous bootstrap for Celery workers.
    Builds the same IoC container used by FastAPI,
    but without depending on FastAPI lifespan.
    """
    try:
        logger.info("[Worker] Bootstrapping IoC container...")

        container = Container()
        register_singletons(container)
        register_services(container)
        register_controllers(container)

        await container.build()
        logger.info("[Worker] IoC container initialized.")
        return container
    except Exception as e:
        logger.error(f"[Worker] Container bootstrap failed: {e}")
        raise


container = asyncio.run(async_bootstrap_worker())
