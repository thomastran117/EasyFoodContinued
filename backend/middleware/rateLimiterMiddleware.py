from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from utilities.logger import logger


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces tiered rate limits:
      - Auth limiter for login/signup
      - Light limiter for refresh/files/images
      - General limiter for all other requests
    """

    def __init__(
        self,
        app,
        general_limit: int = 100,
        general_window: int = 60,
        auth_limit: int = 5,
        auth_window: int = 60,
        light_limit: int = 30,
        light_window: int = 60,
        excluded_paths: Optional[list[str]] = None,
    ):
        super().__init__(app)
        self.general_limit = general_limit
        self.general_window = general_window
        self.auth_limit = auth_limit
        self.auth_window = auth_window
        self.light_limit = light_limit
        self.light_window = light_window
        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        try:
            container = request.app.state.container
            cache_service = await container.resolve("CacheService")
        except Exception as e:
            logger.error(f"[RateLimiter] Failed to resolve CacheService: {e}")
            return await call_next(request)

        limiter_type, limit, window = self._determine_limiter(path)
        client_id = self._identify_client(request)
        key = f"ratelimit:{limiter_type}:{client_id}:{path}"

        try:
            redis = cache_service.client
            count = await redis.incr(key)
            if count == 1:
                await redis.expire(key, window)

            if count > limit:
                logger.warning(
                    f"[RateLimiter] Limit exceeded for {client_id} on {path}"
                )
                raise HTTPException(
                    status_code=429,
                    detail=f"Too many requests ({limiter_type}): limit {limit} per {window}s",
                )

        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": exc.detail},
            )

        except Exception as e:
            logger.error(f"[RateLimiter] Unexpected error: {e}")
            return await call_next(request)

        return await call_next(request)

    def _determine_limiter(self, path: str) -> tuple[str, int, int]:
        """Select limiter type and parameters based on the path."""
        if path.startswith("/api/"):
            path = path[4:]

        if path.startswith("/auth/") and not path.startswith("/auth/refresh"):
            return ("auth", self.auth_limit, self.auth_window)
        elif (
            path.startswith("/auth/refresh")
            or path.startswith("/files")
            or path.startswith("/images")
        ):
            return ("light", self.light_limit, self.light_window)
        else:
            return ("general", self.general_limit, self.general_window)

    def _identify_client(self, request: Request) -> str:
        """Identify client based on IP (or header if desired)."""
        return request.client.host or "unknown"
