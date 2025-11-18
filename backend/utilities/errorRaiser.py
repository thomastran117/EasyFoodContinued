from fastapi import HTTPException

from utilities.logger import logger


class AppHttpException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class BadRequestException(AppHttpException):
    def __init__(self, detail="Bad request"):
        super().__init__(400, detail)


class UnauthorizedException(AppHttpException):
    def __init__(self, detail="Unauthorized"):
        super().__init__(401, detail)


class ForbiddenException(AppHttpException):
    def __init__(self, detail="Forbidden"):
        super().__init__(403, detail)


class NotFoundException(AppHttpException):
    def __init__(self, detail="Not found"):
        super().__init__(404, detail)


class ConflictException(AppHttpException):
    def __init__(self, detail="Conflict"):
        super().__init__(409, detail)


class InternalErrorException(AppHttpException):
    def __init__(self, detail="Internal server error"):
        super().__init__(500, detail)


class NotImplementedException(AppHttpException):
    def __init__(self, detail="Not implemented"):
        super().__init__(501, detail)


class ServiceUnavailableException(AppHttpException):
    def __init__(self, detail="Service unavailable"):
        super().__init__(503, detail)


def raise_error(e: Exception):
    if isinstance(e, AppHttpException):
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    else:
        logger.error("An unknown error occurred", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
