class UserAlreadyExistsException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class ConflictException(Exception):
    pass


class NotFoundException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class BadRequestException(Exception):
    pass


class NotImplementedException(Exception):
    pass


class ServiceUnavaliableException(Exception):
    pass
