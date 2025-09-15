from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from route.route import serverRouter
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from middleware.httpLogger import HTTPLoggerMiddleware
from middleware.corsMiddleware import setup_cors
from middleware.exceptionMiddleware import setup_exception_handlers
from middleware.rateLimiterMiddleware import RateLimiterMiddleware
from config.envConfig import settings
from utilities.logger import get_logger
import os

logger = get_logger(__name__)

app = FastAPI()

setup_cors(app)
setup_exception_handlers(app)

app.add_middleware(SessionMiddleware, secret_key="dev-session-secret")
app.add_middleware(HTTPLoggerMiddleware)
app.add_middleware(RateLimiterMiddleware, max_requests=100, window=60)

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
    )
