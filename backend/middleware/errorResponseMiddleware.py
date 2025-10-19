from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_400_BAD_REQUEST


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join([str(loc) for loc in err.get("loc", []) if loc not in ("body",)])
        msg = err.get("msg", "Invalid value")
        if field:
            errors.append(f"{field}: {msg}")
        else:
            errors.append(msg)

    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid input",
            "details": errors,
        },
    )
