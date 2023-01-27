"""Requests."""
from typing import Dict as _Dict, Any as _Any, Optional as _Optional
from aio_lambda_api.json import loads as _loads, JSONDecodeError as _JSONDecodeError


class Request:
    """Request."""

    __slots__ = ["_headers", "_body", "_json", "_path", "_method", "_raises_exceptions"]

    def __init__(
        self,
        path: str,
        method: str,
        headers: _Optional[_Dict[str, str]] = None,
        body: _Optional[bytes] = None,
        raises_exceptions: bool = False,
    ) -> None:
        self._headers = (
            {key.lower(): value for key, value in headers.items()}
            if headers
            else dict()
        )
        if body is not None:
            self._body = body
        self._path = path
        self._method = method
        self._raises_exceptions = raises_exceptions

    @property
    def path(self) -> str:
        """HTTP route path.

        Returns:
            Path.
        """
        return self._path

    @property
    def method(self) -> str:
        """HTTP method.

        Returns:
            Method.
        """
        return self._method

    @property
    def headers(self) -> _Dict[str, str]:
        """HTTP headers.

        Returns:
            Headers.
        """
        return self._headers

    async def body(self) -> _Optional[bytes]:
        """Body.

        Returns:
            Body.
        """
        try:
            return self._body
        except AttributeError:
            return None

    async def json(self) -> _Any:
        """JSON body.

        Returns:
            JSON deserialized body.
        """
        try:
            return self._json
        except AttributeError:
            body = await self.body()
            if body is not None:
                try:
                    body = _loads(body)
                except _JSONDecodeError:
                    pass
            self._json: _Any = body
            return body

    @property
    def server_id(self) -> _Optional[str]:
        """Server ID.

        Returns:
            Server ID.
        """
        return None

    @property
    def raises_exceptions(self) -> bool:
        """If True, raises exceptions.

        Returns:
            Boolean.
        """
        return self._raises_exceptions
