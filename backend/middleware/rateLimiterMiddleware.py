import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from resources.redisDb import redis_client


class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int = 100, window: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        key = f"rate_limit:{ip}"

        current = redis_client.incr(key)
        if current == 1:
            redis_client.expire(key, self.window)

        if current > self.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Too Many Requests: limit {self.max_requests} per {self.window}s",
            )

        return await call_next(request)
