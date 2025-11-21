import inspect
from abc import ABC

from utilities.errorRaiser import InternalErrorException, ServiceUnavailableException
from utilities.logger import logger


class BaseService(ABC):
    """
    Base class for all services.
    Cannot be instantiated directly — must be subclassed.
    """

    def __init__(self):
        if type(self) is BaseService:
            raise TypeError(
                "BaseService cannot be instantiated directly. Inherit from it instead."
            )

    def ensureDependencies(self, *required_deps: str):
        try:
            caller = inspect.stack()[1].function

            for dep_name in required_deps:
                dep = getattr(self, dep_name, None)
                if dep is None:
                    logger.error(
                        f"[{self.__class__.__name__}] {caller} failed. "
                        f"{dep_name} is not available"
                    )
                    raise ServiceUnavailableException(
                        "Service is not ready to handle this request"
                    )

        except Exception as e:
            logger.error(f"[BaseService] ensureDependencies failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
