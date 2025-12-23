import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from config.environmentConfig import settings
from container.containerBootstrap import bootstrap
from middleware.errorHandlerMiddleware import setup_exception_handlers
from middleware.httpLogger import HTTPLoggerMiddleware
from middleware.rateLimiterMiddleware import RateLimiterMiddleware
from middleware.securityMiddleware import (
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
    setup_cors,
)
from route.route import serverRouter
from utilities.errorRaiser import AppHttpException
from utilities.logger import logger


def register_app_exceptions(app: FastAPI):
    @app.exception_handler(AppHttpException)
    async def app_exception_handler(request, exc: AppHttpException):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        container = await bootstrap()
        app.state.container = container
        port = int(settings.port)
        logger.info(f"Server starting at http://localhost:{port}")
        yield
    except Exception as e:
        logger.error(f"[Server] Container startup failed: {e}", exc_info=True)
        raise


app = FastAPI(title="EasyFood", lifespan=lifespan)

register_app_exceptions(app)
setup_cors(app)
setup_exception_handlers(app)

app.add_middleware(RateLimiterMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(RequestIDMiddleware)


@app.middleware("http")
async def createRequestScope(request: Request, call_next):
    container = request.app.state.container

    async with container.create_scope() as scope:
        request.state.scope = scope

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"[Scope] Error during request: {e}", exc_info=True)
            raise

        try:
            logger.info(f"[Scope] Resolved services: {list(scope.keys())}")
            for name, instance in scope.items():
                logger.info(f"[Scope] {name}: {type(instance).__name__}")
        except Exception as e:
            logger.error(f"[Scope] Failed to inspect scope: {e}")

        return response


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
    try:
        port = int(settings.port)

        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=port,
            access_log=False,
        )

    except Exception as e:
        logger.error(f"[Server] Application failed to start: {e}", exc_info=True)
