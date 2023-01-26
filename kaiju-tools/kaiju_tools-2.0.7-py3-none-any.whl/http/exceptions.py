from aiohttp.web import middleware, Response, Request
from aiohttp.web_exceptions import *

from ..exceptions import APIException
from ..serialization import dumps

__all__ = ['error_middleware']


@middleware
async def error_middleware(request: Request, handler):
    """Wrap a HTTP error."""
    try:
        return await handler(request)
    except Exception as exc:
        if isinstance(exc, APIException):
            error = exc
        elif isinstance(exc, HTTPClientError):
            error = APIException(message=str(exc), base_exc=exc)
            error.status_code = exc.status
        else:
            error = APIException(message=str(exc), base_exc=exc)
        return Response(
            status=error.status_code,
            text=dumps({'jsonrpc': '2.0', 'id': None, 'error': error.repr()}),  # RPC compatibility (kinda)
            headers={},
            content_type='application/json',
        )
