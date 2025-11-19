import inspect

from utilities.errorRaiser import InternalErrorException, ServiceUnavailableException
from utilities.logger import logger


class BaseService:
    """
    Provides dependency validation helpers to all services.
    Any service that inherits this can call `self.ensure_ready(...)`
    to validate that required dependencies exist.
    """

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
        except:
            logger.error(f"[BaseService] ensureDependencies failed: {e}", exc_info=True)
            raise InternalErrorException("Internal server error")
