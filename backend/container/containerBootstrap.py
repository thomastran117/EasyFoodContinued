from utilities.logger import logger

from .container import Container
from .containerControllers import register_controllers
from .containerCore import register_singletons
from .containerServices import register_services


async def bootstrap() -> Container:
    logger.info("Bootstrapping IoC container asynchronously...")

    container = Container()
    register_singletons(container)
    register_services(container)
    register_controllers(container)

    await container.build()
    container.summary()
    logger.info("IoC container Bootstrap completed.")
    return container
