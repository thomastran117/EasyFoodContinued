from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from resources.redis_client import redis_client


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        default_limit: int = 100,
        default_window: int = 60,
        auth_limit: int = 5,
        auth_window: int = 60,
        excluded_paths: list[str] | None = None,
    ):
        super().__init__(app)
        self.default_limit = default_limit
        self.default_window = default_window
        self.auth_limit = auth_limit
        self.auth_window = auth_window
        self.excluded_paths = excluded_paths or []

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in self.excluded_paths):
            return await call_next(request)

        if path.startswith("/auth/") and not path.startswith("/auth/refresh"):
            max_requests = self.auth_limit
            window = self.auth_window
        else:
            max_requests = self.default_limit
            window = self.default_window

        ip = request.client.host
        key = f"rate_limit:{path}:{ip}"

        try:
            current = redis_client.incr(key)
            if current == 1:
                redis_client.expire(key, window)

            if current > max_requests:
                raise HTTPException(
                    status_code=429,
                    detail=f"Too Many Requests: limit {max_requests} per {window}s for this route",
                )
        except Exception:
            return await call_next(request)

        return await call_next(request)
