import os
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
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
from container.containerBootstrap import bootstrap
from resources.mongo_client import init_mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Waiting for IoC container...")
    await init_mongo()
    container = await bootstrap()
    app.state.container = container
    logger.info("Container ready.")

    yield

    logger.info("Cleaning up IoC resources...")
    with container.create_scope() as scope:
        for instance in scope.values():
            close_fn = getattr(instance, "close", None)
            if callable(close_fn):
                close_fn()
    logger.info("Cleanup done.")


app = FastAPI(title="EasyFood", lifespan=lifespan)

setup_cors(app)
setup_exception_handlers(app)
"""
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
"""
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(RequestIDMiddleware)

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
if os.path.isdir(PUBLIC_DIR):
    app.mount("/public", StaticFiles(directory=PUBLIC_DIR), name="public")
else:
    logger.warning("Static directory %s not found; skipping mount.", PUBLIC_DIR)

app.include_router(serverRouter, prefix="/api")


@app.get("/")
def read_root():
    return FileResponse("public/index.html")


@app.get("/ping")
def ping():
    return "pong"


@app.get("/health")
def health():
    return "ok"


if __name__ == "__main__":
    port = int(settings.port)
    logger.info(f"Server starting at http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, access_log=False)
