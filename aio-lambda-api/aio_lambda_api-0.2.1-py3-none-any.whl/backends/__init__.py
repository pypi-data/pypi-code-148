"""Backends."""
from abc import abstractmethod as _abstractmethod, ABC as _ABC
from asyncio import gather as _gather
from importlib import import_module as _import_module
from typing import (
    Dict as _Dict,
    Any as _Any,
    List as _List,
    Union as _Union,
    Iterable as _Iterable,
    Tuple as _Tuple,
    Optional as _Optional,
)
from aio_lambda_api.json import dumps as _dumps
from aio_lambda_api.requests import Request as _Request
from aio_lambda_api.responses import Response as _Response
from aio_lambda_api.settings import BACKEND as _BACKEND


class BackendBase(_ABC):
    """Backend base."""

    @staticmethod
    async def emit_log(log: _Dict[str, _Any]) -> None:
        """Emit log.

        Args:
            log: Log object.
        """
        print(_dumps(log))

    @_abstractmethod
    async def parse_request(
        self, *args: _Any, **kwargs: _Any
    ) -> _Union[_Request, _List[_Request]]:
        """Parse request(s).

        Returns:
            Request(s).
        """

    @_abstractmethod
    async def serialize_response(self, response: _Response, request: _Request) -> _Any:
        """Serialize response.

        Args:
            response: Response.
            request: Request.

        Returns:
            Serialized response.
        """

    async def serialize_responses(
        self, resp_req: _Iterable[_Tuple[_Response, _Request]]
    ) -> _Any:
        """Serialize response.

        Args:
            resp_req: Response & request.

        Returns:
            Serialized response.
        """
        return _gather(
            *(
                self.serialize_response(response, request)
                for response, request in resp_req
            )
        )


def get_backend(name: _Optional[str]) -> BackendBase:
    """Import backend.

    Args:
        name: Backend name.

    Returns:
        Backend class.
    """
    name = name or _BACKEND
    element = f"aio_lambda_api.backends.{name}"
    try:
        module = _import_module(element)
    except ImportError:
        from importlib.util import find_spec

        if find_spec(element) is not None:  # pragma: no cover
            raise
        raise NotImplementedError(f"Unsupported backend: {name}")
    return getattr(module, "Backend")()  # type: ignore
