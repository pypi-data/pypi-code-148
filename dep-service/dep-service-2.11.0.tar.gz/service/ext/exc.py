"""Service helpers."""

from fastapi.exceptions import HTTPException  # noqa
from pydantic import BaseModel


class ErrorUnknown(BaseModel):
    """Unknown."""

    detail: str = 'Oups, something went wrong'


class ErrorNotFound(ErrorUnknown):
    """Not found error - 404."""

    detail: str = 'Not found'


class ErrorBadRequest(ErrorUnknown):
    """Bad request - 400."""

    detail: str = 'Bad request'


class ErrorUnauthorized(ErrorUnknown):
    """Unauthorized error - 401."""

    detail: str = 'Unauthorized'


class ErrorForbidden(ErrorUnknown):
    """Unauthorized error - 403."""

    detail: str = 'Forbidden'
