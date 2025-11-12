from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import timedelta

from container.containerEntry import container
from service.cacheService import CacheService


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """
    Middleware that enforces tiered rate limits:
      - Auth limiter for login/signup
      - Refresh/File limiter for light requests
      - General limiter for everything else
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
        excluded_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.general_limit = general_limit
        self.general_window = general_window
        self.auth_limit = auth_limit
        self.auth_window = auth_window
        self.light_limit = light_limit
        self.light_window = light_window
        self.excluded_paths = excluded_paths or []

        self.cache: CacheService = container.resolve("CacheService")

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        limiter_type, limit, window = self._determine_limiter(path)
        client_id = self._identify_client(request)
        key = f"ratelimit:{limiter_type}:{client_id}:{path}"

        try:
            count = self.cache.client.incr(key)
            if count == 1:
                self.cache.client.expire(key, window)

            if count > limit:
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
            # fallback for unexpected issues
            return await call_next(request)

        return await call_next(request)

    def _determine_limiter(self, path: str) -> tuple[str, int, int]:
        """Select limiter type and parameters based on the path."""
        if path.startswith("/api/"):
            path = path[4:]

        if path.startswith("/auth/") and not path.startswith("/auth/refresh"):
            return ("auth", self.auth_limit, self.auth_window)
        elif path.startswith("/auth/refresh") or path.startswith("/files") or path.startswith("/images"):
            return ("light", self.light_limit, self.light_window)
        else:
            return ("general", self.general_limit, self.general_window)

    def _identify_client(self, request: Request) -> str:
        ip = request.client.host or "unknown"
        auth_header = request.headers.get("authorization")
        return ip
