import logging
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from the_spymaster_util.http.defs import ErrorTypes

log = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(
        self,
        message: str = "Internal server error",
        status_code: int = 500,
        details: Optional[dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class BadRequestError(ApiError):
    def __init__(self, message: str, status_code: int = 400, details: Optional[dict] = None):
        super().__init__(message=message, status_code=status_code, details=details)


class UnauthorizedError(BadRequestError):
    def __init__(self, message: str, status_code: int = 401, details: Optional[dict] = None):
        super().__init__(message=message, status_code=status_code, details=details)


class ForbiddenError(BadRequestError):
    def __init__(self, message: str, status_code: int = 403, details: Optional[dict] = None):
        super().__init__(message=message, status_code=status_code, details=details)


class NotFoundError(BadRequestError):
    def __init__(self, message: str, status_code: int = 404, details: Optional[dict] = None):
        super().__init__(message=message, status_code=status_code, details=details)


DEFAULT_ERRORS: "ErrorTypes" = frozenset({ApiError, BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError})
