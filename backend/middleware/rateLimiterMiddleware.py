import time
from typing import Optional, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from service.cacheService import CacheService
from utilities.logger import logger


class RateLimitStore:
    """
    Storage abstraction for rate limiting.
    Fail-open by design.
    """

    def __init__(self, cache: CacheService):
        self.cache = cache

    async def consume_token(
        self,
        key: str,
        capacity: int,
        rate: float,
    ) -> Tuple[bool, float]:
        """
        Returns (allowed, retry_after_seconds)
        """
        now = time.time()

        try:
            bucket = await self.cache.get(key, as_json=True) or {}
            tokens = float(bucket.get("tokens", capacity))
            last_ts = float(bucket.get("ts", now))

            elapsed = max(0.0, now - last_ts)
            tokens = min(capacity, tokens + elapsed * rate)

            if tokens < 1:
                retry_after = (1 - tokens) / rate
                return False, retry_after

            tokens -= 1

            await self.cache.set(
                key,
                {"tokens": tokens, "ts": now},
                expire=int(2 * capacity / rate),
                as_json=True,
            )

            return True, 0.0

        except Exception as e:
            logger.warn(f"[RateLimitStore] failure — fail open: {e}")
            return True, 0.0


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Token-bucket rate limiter.
    FAIL-OPEN if cache/storage is unavailable.
    """

    def __init__(
        self,
        app,
        general_capacity: int = 100,
        general_refill_window: int = 60,
        auth_capacity: int = 5,
        auth_refill_window: int = 60,
        light_capacity: int = 30,
        light_refill_window: int = 60,
        excluded_paths: Optional[list[str]] = None,
    ):
        super().__init__(app)
        self.excluded_paths = excluded_paths or []

        self.general_capacity = general_capacity
        self.auth_capacity = auth_capacity
        self.light_capacity = light_capacity

        self.general_rate = general_capacity / general_refill_window
        self.auth_rate = auth_capacity / auth_refill_window
        self.light_rate = light_capacity / light_refill_window

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        try:
            container = request.app.state.container
            cache_service = await container.resolve("CacheService")
            store = RateLimitStore(cache_service)
        except Exception as e:
            logger.warn(f"[RateLimiter] Cache unavailable — bypassing: {e}")
            return await call_next(request)

        limiter_type, capacity, rate = self._determine_limiter(path)
        client_id = request.client.host or "unknown"

        key = f"ratelimit:{limiter_type}:{client_id}"

        allowed, retry_after = await store.consume_token(
            key=key,
            capacity=capacity,
            rate=rate,
        )

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": f"Rate limit exceeded ({limiter_type})",
                    "retry_after": round(retry_after, 2),
                },
                headers={"Retry-After": str(int(retry_after))},
            )

        return await call_next(request)

    def _determine_limiter(self, path: str) -> tuple[str, int, float]:
        if path.startswith("/api/"):
            path = path[4:]

        if path.startswith("/auth/") and not path.startswith("/auth/refresh"):
            return ("auth", self.auth_capacity, self.auth_rate)

        if path.startswith("/auth/refresh") or path.startswith("/files"):
            return ("light", self.light_capacity, self.light_rate)

        return ("general", self.general_capacity, self.general_rate)
