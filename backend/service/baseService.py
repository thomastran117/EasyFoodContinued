import inspect

from utilities.errorRaiser import ServiceUnavaliableException
from utilities.logger import logger


class BaseService:
    """
    Provides dependency validation helpers to all services.
    Any service that inherits this can call `self.ensure_ready(...)`
    to validate that required dependencies exist.
    """

    def ensureDependencies(self, *required_deps: str):
        caller = inspect.stack()[1].function

        for dep_name in required_deps:
            dep = getattr(self, dep_name, None)
            if dep is None:
                logger.error(
                    f"[{self.__class__.__name__}] {caller} failed. "
                    f"{dep_name} is not available"
                )
                raise ServiceUnavaliableException(
                    "Service is not ready to handle this request"
                )
