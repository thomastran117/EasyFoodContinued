import time
from typing import Optional, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse
from jose import JWTError
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
    def __init__(
        self,
        app,
        general_capacity: int = 100,
        general_refill_window: int = 60,
        auth_capacity: int = 5,
        auth_refill_window: int = 60,
        excluded_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.excluded_paths = excluded_paths or []

        self.general_capacity = general_capacity
        self.auth_capacity = auth_capacity

        self.general_rate = general_capacity / general_refill_window
        self.auth_rate = auth_capacity / auth_refill_window

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        # --------------------------------------------------
        # Resolve CacheService (fail-open)
        # --------------------------------------------------
        try:
            container = request.app.state.container
            cache = await container.resolve("CacheService")
            store = RateLimitStore(cache)
        except Exception as e:
            logger.warn(f"[RateLimiter] Cache unavailable — bypassing: {e}")
            return await call_next(request)

        # --------------------------------------------------
        # Determine identity (user > ip)
        # --------------------------------------------------
        identity = self._resolve_identity(request)

        limiter_type, capacity, rate = self._determine_limiter(path)
        key = f"ratelimit:{limiter_type}:{identity}"

        allowed, retry_after = await store.consume_token(
            key=key,
            capacity=capacity,
            rate=rate,
        )

        if not allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": round(retry_after, 2),
                },
                headers={"Retry-After": str(int(retry_after))},
            )

        return await call_next(request)

    def _resolve_identity(self, request: Request) -> str:
        auth = request.headers.get("authorization")

        if auth and auth.startswith("Bearer "):
            token = auth[7:]
            try:
                container = request.app.state.container
                token_service = container.resolve_sync("BasicTokenService")
                payload = token_service.decodeAccessToken(token)

                user_id = payload["id"]
                if user_id:
                    return f"user:{user_id}"

            except Exception:
                pass

        ip = request.client.host if request.client else "unknown"
        return f"ip:{ip}"

    def _determine_limiter(self, path: str):
        if path.startswith("/api/auth/"):
            return ("auth", self.auth_capacity, self.auth_rate)

        return ("general", self.general_capacity, self.general_rate)
