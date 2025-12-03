import time
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from utilities.logger import logger


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Token-bucket rate limiter with tiered limits.
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

        self.general_rate = general_capacity / general_refill_window
        self.auth_rate = auth_capacity / auth_refill_window
        self.light_rate = light_capacity / light_refill_window

        self.general_capacity = general_capacity
        self.auth_capacity = auth_capacity
        self.light_capacity = light_capacity

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        try:
            container = request.app.state.container
            cache_service = await container.resolve("CacheService")
            redis = cache_service.client
        except Exception as e:
            logger.error(f"[RateLimiter] Failed to resolve CacheService: {e}")
            return await call_next(request)

        limiter_type, capacity, rate = self._determine_limiter(path)

        client_id = request.client.host or "unknown"
        key = f"ratelimit:{limiter_type}:{client_id}"

        now = time.time()

        try:
            bucket = await redis.hgetall(key)
            tokens = float(bucket.get(b"tokens", capacity))
            last_ts = float(bucket.get(b"ts", now))

            elapsed = now - last_ts
            tokens = min(capacity, tokens + elapsed * rate)

            if tokens < 1:
                retry_after = (1 - tokens) / rate

                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": f"Rate limit exceeded ({limiter_type})",
                        "retry_after": round(retry_after, 2),
                    },
                    headers={"Retry-After": str(int(retry_after))},
                )

            tokens -= 1

            await redis.hset(key, mapping={"tokens": tokens, "ts": now})
            await redis.expire(key, 2 * int(capacity / rate))

        except Exception as e:
            logger.error(f"[RateLimiter] Unexpected Redis error: {e}")
            return await call_next(request)

        return await call_next(request)

    def _determine_limiter(self, path: str) -> tuple[str, int, float]:
        """Return limiter type, bucket capacity, refill rate."""

        if path.startswith("/api/"):
            path = path[4:]

        if path.startswith("/auth/") and not path.startswith("/auth/refresh"):
            return ("auth", self.auth_capacity, self.auth_rate)

        elif (
            path.startswith("/auth/refresh")
            or path.startswith("/files")
            or path.startswith("/images")
        ):
            return ("light", self.light_capacity, self.light_rate)

        return ("general", self.general_capacity, self.general_rate)
