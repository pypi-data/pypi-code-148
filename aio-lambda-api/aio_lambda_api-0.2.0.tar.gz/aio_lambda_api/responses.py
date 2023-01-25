"""Responses."""
from typing import Optional as _Optional, Any as _Any, Dict as _Dict, Union as _Union
from aio_lambda_api.json import dumps as _dumps
from aio_lambda_api.status import get_status_message as _get_status_message
from aio_lambda_api.logging import context_log as _context_log


Body = _Union[str, bytes, bytearray, memoryview]


class Response:
    """Response."""

    _MEDIA_TYPE: _Optional[str] = None
    charset = "utf-8"

    __slots__ = ["_content", "_status_code", "_headers", "_media_type"]

    def __init__(
        self,
        content: _Optional[_Any] = None,
        status_code: int = 200,
        headers: _Optional[_Dict[str, str]] = None,
        media_type: _Optional[str] = None,
    ) -> None:
        self._content = content
        self._media_type = media_type or self._MEDIA_TYPE
        self.status_code = status_code
        self._headers = headers or dict()
        log = _context_log.get()
        try:
            self._headers["x-request-id"] = log["request_id"]
        except KeyError:
            pass

    @property
    def headers(self) -> _Dict[str, str]:
        """HTTP headers.

        Returns:
            Headers.
        """
        return self._headers

    @property
    def status_code(self) -> int:
        """HTTP Status code.

        Returns:
            Status code.
        """
        return self._status_code

    @status_code.setter
    def status_code(self, value: int) -> None:
        """HTTP Status code.

        Args:
            value: Status code.
        """
        if self._content is None and value == 200:
            value = 204
        self._status_code = _context_log.get()["status_code"] = value

    @property
    def content(self) -> _Any:
        """Response content.

        Returns:
            Content.
        """
        return self._content

    @content.setter
    def content(self, value: _Any) -> None:
        """Response content.

        Args:
            value: Content.
        """
        self._content = value
        if value is not None and self._status_code == 204:
            self._status_code = _context_log.get()["status_code"] = 200

    async def _render(self, content: _Any) -> Body:
        """Render content for response in str or bytes.

        Args:
            content: Body content.

        Returns:
            Rendered content.
        """
        return content  # type: ignore

    async def body(self) -> _Optional[Body]:
        """Body.

        Returns:
            Rendered body.
        """
        body: _Optional[Body] = None

        if self._content is None and self._status_code >= 400:
            self._content = dict(details=_get_status_message(self._status_code))

        if self._content is not None:
            body = await self._render(self._content)
            self._headers["content-length"] = str(len(body))
            if self._media_type is not None:
                self._headers["content-type"] = self._media_type

        return body


class JSONResponse(Response):
    """JSON Response."""

    _MEDIA_TYPE = "application/json"

    async def _render(self, content: _Any) -> str:
        """Render content for response in JSON str.

        Args:
            content: Body content.

        Returns:
            JSON content.
        """
        return _dumps(content)
