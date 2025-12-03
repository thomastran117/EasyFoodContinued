import asyncio
from typing import Any, Awaitable, Callable, Optional

from sqlalchemy.exc import DBAPIError, IntegrityError, OperationalError

from utilities.logger import logger


class BaseRepository:
    """
    Base class for all repositories. Provides:
      - transient DB/network error detection
      - exponential-backoff retries
    """

    def isTransient(self, e: Exception) -> bool:
        """
        Returns True only for network-related or database transient failures
        that are safe to retry.
        """
        if isinstance(e, OperationalError):
            return True

        if isinstance(e, DBAPIError) and getattr(e, "connection_invalidated", False):
            return True

        return False

    async def retry(
        self,
        func: Callable[[], Awaitable[Any]],
        retries: int = 3,
        backoff: float = 0.25,
        factor: float = 2.0,
    ):
        """
        Execute `func` with retry on transient errors.

        Will NOT retry on:
          - IntegrityError (unique constraint, FK violation)
          - Programming or logical errors
          - Unknown fatal errors
        """
        attempt = 0

        while True:
            try:
                return await func()

            except IntegrityError:
                raise

            except Exception as e:
                if attempt >= retries or not self.isTransient(e):
                    logger.error(
                        f"[Repository Retry] Non-retriable or max retries exceeded: {e}"
                    )
                    raise

                sleep_time = backoff * (factor**attempt)
                logger.warning(
                    f"[Repository Retry] Transient DB error ({e.__class__.__name__}): "
                    f"retrying in {sleep_time:.2f}s (attempt {attempt + 1}/{retries})"
                )
                await asyncio.sleep(sleep_time)
                attempt += 1
