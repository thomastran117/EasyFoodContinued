import asyncio
from utilities.logger import logger
from container.container import Container
from container.containerCore import register_singletons
from container.containerServices import register_services
from container.containerControllers import register_controllers


async def async_bootstrap_worker() -> Container:
    """
    Asynchronous bootstrap for Celery workers.
    Builds the same IoC container used by FastAPI,
    but without depending on FastAPI lifespan.
    """
    logger.info("[Worker] Bootstrapping IoC container...")

    container = Container()
    register_singletons(container)
    register_services(container)
    register_controllers(container)

    await container.build()
    logger.info("[Worker] IoC container initialized.")
    return container


logger.info("[Worker] Initializing container at import time...")
container = asyncio.run(async_bootstrap_worker())
logger.info("[Worker] Container ready for Celery tasks.")
