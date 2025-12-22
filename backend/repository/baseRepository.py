import asyncio
from typing import Any, Awaitable, Callable

from pymongo.errors import (
    AutoReconnect,
    NetworkTimeout,
    NotPrimaryError,
    ServerSelectionTimeoutError,
    PyMongoError,
    DuplicateKeyError,
    OperationFailure,
)

from utilities.logger import logger


class BaseRepository:
    """
    Base class for all repositories (MongoDB).

    Provides:
      - transient MongoDB error detection
      - exponential-backoff retries
    """

    def isTransient(self, e: Exception) -> bool:
        """
        Returns True only for MongoDB transient failures
        that are safe to retry.
        """

        if isinstance(
            e,
            (
                AutoReconnect,
                NetworkTimeout,
                NotPrimaryError,
                ServerSelectionTimeoutError,
            ),
        ):
            return True

        if isinstance(e, PyMongoError):
            labels = getattr(e, "error_labels", None)
            if labels and "TransientTransactionError" in labels:
                return True
            if labels and "RetryableWriteError" in labels:
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
        Execute `func` with retry on MongoDB transient errors.

        Will NOT retry on:
          - DuplicateKeyError (unique index violation)
          - Validation / logical errors
          - Non-transient PyMongo errors
        """
        attempt = 0

        while True:
            try:
                return await func()

            except DuplicateKeyError:
                raise

            except OperationFailure as e:
                if e.code == 11000:
                    raise

                if not self.isTransient(e):
                    logger.error(
                        f"[Repository Retry] Non-retriable Mongo error: {e}",
                        exc_info=True,
                    )
                    raise

            except Exception as e:
                if not self.isTransient(e) or attempt >= retries:
                    logger.error(
                        f"[Repository Retry] Non-retriable or max retries exceeded: {e}",
                        exc_info=True,
                    )
                    raise

            sleep_time = backoff * (factor**attempt)
            logger.warn(
                f"[Repository Retry] Transient Mongo error "
                f"({e.__class__.__name__}): retrying in {sleep_time:.2f}s "
                f"(attempt {attempt + 1}/{retries})"
            )
            await asyncio.sleep(sleep_time)
            attempt += 1
