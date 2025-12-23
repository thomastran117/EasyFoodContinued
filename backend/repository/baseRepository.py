import asyncio
import random
from typing import Any, Awaitable, Callable

from pymongo.errors import (
    AutoReconnect,
    DuplicateKeyError,
    NetworkTimeout,
    NotPrimaryError,
    OperationFailure,
    PyMongoError,
    ServerSelectionTimeoutError,
)

from utilities.circuitBreaker import CircuitBreaker
from utilities.logger import logger


class BaseRepository:
    """
    MongoDB repository base with:
      - retry + exponential backoff
      - jitter
      - circuit breaker
      - clear retry semantics
    """

    def __init__(
        self,
        *,
        retries: int = 3,
        base_delay: float = 0.25,
        backoff_factor: float = 2.0,
        max_delay: float = 5.0,
        circuit_breaker: CircuitBreaker | None = None,
    ):
        self.retries = retries
        self.base_delay = base_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.breaker = circuit_breaker or CircuitBreaker()

    def is_transient(self, e: Exception) -> bool:
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
            labels = getattr(e, "error_labels", None) or set()
            return (
                "TransientTransactionError" in labels or "RetryableWriteError" in labels
            )

        return False

    def is_non_retriable(self, e: Exception) -> bool:
        if isinstance(e, DuplicateKeyError):
            return True

        if isinstance(e, OperationFailure) and e.code == 11000:
            return True

        return False

    async def executeAsync(
        self,
        func: Callable[[], Awaitable[Any]],
        *,
        retries: int | None = None,
    ) -> Any:
        if not self.breaker.allow():
            raise RuntimeError("MongoDB circuit breaker OPEN — fast failing")

        attempts = retries if retries is not None else self.retries
        attempt = 0

        while True:
            try:
                result = await func()
                self.breaker.record_success()
                return result

            except Exception as e:
                if self.is_non_retriable(e):
                    logger.debug(
                        "[Repository] Non-retriable Mongo error",
                        exc_info=True,
                    )
                    raise

                if not self.is_transient(e) or attempt >= attempts:
                    self.breaker.record_failure()
                    logger.error(
                        "[Repository] Mongo operation failed",
                        exc_info=True,
                    )
                    raise

                delay = min(
                    self.base_delay * (self.backoff_factor**attempt),
                    self.max_delay,
                )

                delay *= random.uniform(0.8, 1.2)

                logger.warning(
                    f"[Repository Retry] Transient Mongo error "
                    f"({e.__class__.__name__}) — retrying in {delay:.2f}s "
                    f"(attempt {attempt + 1}/{attempts})"
                )

                await asyncio.sleep(delay)
                attempt += 1
