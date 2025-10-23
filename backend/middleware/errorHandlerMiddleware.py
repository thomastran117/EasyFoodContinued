from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_400_BAD_REQUEST
from utilities.errorRaiser import raise_error
from utilities.logger import get_logger

logger = get_logger(__name__)


class GlobalErrorMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Unhandled exception: {repr(e)}")
            return raise_error(e)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join([str(loc) for loc in err.get("loc", []) if loc != "body"])
        msg = err.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}" if field else msg)

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid input",
            "details": errors,
        },
    )


def setup_exception_handlers(app: FastAPI):
    app.add_middleware(GlobalErrorMiddleware)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
