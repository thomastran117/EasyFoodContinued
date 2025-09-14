from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Bad Request: Invalid input",
            "errors": exc.errors(),
        },
    )


def setup_exception_handlers(app):
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
