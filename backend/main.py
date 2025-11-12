import os

import uvicorn
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from config.environmentConfig import settings
from middleware.errorHandlerMiddleware import setup_exception_handlers
from middleware.httpLogger import HTTPLoggerMiddleware
from middleware.rateLimiterMiddleware import RateLimiterMiddleware
from middleware.securityMiddleware import (
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    setup_cors,
)
from route.route import serverRouter
from utilities.logger import logger

app = FastAPI()

setup_cors(app)
setup_exception_handlers(app)

app.add_middleware(
    RateLimiterMiddleware,
    general_limit=100,
    general_window=60,
    auth_limit=5,
    auth_window=60,
    light_limit=100,
    light_window=60,
    excluded_paths=["/docs", "/openapi.json"],
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(RequestIDMiddleware)

setup_exception_handlers(app)

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
if os.path.isdir(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")
else:
    logger.warning("Static directory %s not found; skipping mount.", PUBLIC_DIR)

app.include_router(serverRouter, prefix="/api")


@app.get("/")
def read_root():
    return FileResponse("public/index.html")


@app.get("/api")
def api_check():
    return "EasyFood API is running"


@app.get("/ping")
def api_check():
    return "pong"


@app.get("/health")
def api_check():
    return "Health check is ok!"


if __name__ == "__main__":
    port = int(settings.port)
    logger.info(f"Server starting at http://localhost:{port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        access_log=False,
        # reload=True,
    )
