from fastapi import HTTPException
from utilities.exception import (
    ConflictException,
    BadRequestException,
    UnauthorizedException,
    NotFoundException,
    ForbiddenException,
    NotImplementedException,
    ServiceUnavaliableException,
)
from utilities.logger import logger


def raise_error(e: Exception):
    if isinstance(e, BadRequestException):
        raise HTTPException(status_code=400, detail=str(e))
    elif isinstance(e, UnauthorizedException):
        raise HTTPException(status_code=401, detail=str(e))
    elif isinstance(e, ForbiddenException):
        raise HTTPException(status_code=403, detail=str(e))
    elif isinstance(e, NotFoundException):
        raise HTTPException(status_code=404, detail=str(e))
    elif isinstance(e, ConflictException):
        raise HTTPException(status_code=409, detail=str(e))
    elif isinstance(e, NotImplementedException):
        raise HTTPException(status_code=501, detail=str(e))
    elif isinstance(e, ServiceUnavaliableException):
        raise HTTPException(status_code=503, detail=str(e))
    else:
        logger.error("Unhandled exception occurred", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
