from typing import Iterable
from typing import Optional
from typing import Union

from drakaina.middlewares.base import BaseMiddleware
from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.rpc_protocols import JsonRPCv2
from drakaina.type_annotations import WSGIApplication
from drakaina.type_annotations import WSGIEnvironment
from drakaina.type_annotations import WSGIErrorsStream
from drakaina.type_annotations import WSGIInputStream
from drakaina.type_annotations import WSGIResponse
from drakaina.type_annotations import WSGIStartResponse

ALLOWED_METHODS = ("OPTION", "HEAD", "GET", "POST")


class WSGIHandler(WSGIApplication):
    """Implementation of WSGI protocol.

    :param route:
    :type route: str
    :param handler:
    :type handler: BaseRPCProtocol
    :param middlewares:
    :type middlewares: Iterable[BaseMiddleware]
    :param provide_smd:
    :type provide_smd: bool
    :param provide_openrpc:
    :type provide_openrpc: bool
    :param provide_openapi:
    :type provide_openapi: bool

    """

    environ: WSGIEnvironment
    start_response: WSGIStartResponse

    def __init__(
        self,
        route: Optional[str] = None,
        handler: Optional[BaseRPCProtocol] = None,
        middlewares: Optional[Iterable[BaseMiddleware]] = None,
        provide_smd: Optional[Union[bool, str]] = False,
        provide_openrpc: Optional[Union[bool, str]] = False,
        provide_openapi: Optional[Union[bool, str]] = False,
    ):
        self.handler = handler or JsonRPCv2()
        self.route = route
        self.provide_smd = provide_smd
        self.provide_openrpc = provide_openrpc
        self.provide_openapi = provide_openapi

    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        self.environ = environ
        self.start_response = start_response
        method = environ.get("REQUEST_METHOD").lower()

        if self.route:
            path = environ.get("PATH_INFO")
            if path != self.route:
                return self._not_found()

        if method.upper() in ALLOWED_METHODS:
            return getattr(self, method.lower())()

        return self._method_not_allowed()

    def get(self) -> WSGIResponse:
        if self.provide_smd:
            response_body = self.handler.smd_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
            self.start_response("200 OK", response_headers)
        elif self.provide_openrpc:
            response_body = self.handler.openrpc_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
            self.start_response("200 OK", response_headers)
        elif self.provide_openapi:
            response_body = self.handler.openapi_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
            self.start_response("200 OK", response_headers)
        else:
            return self._method_not_allowed()

        yield response_body

    def post(self) -> WSGIResponse:
        wsgi_input: WSGIInputStream = self.environ.get("wsgi.input")
        wsgi_errors: WSGIErrorsStream = self.environ.get("wsgi.errors")

        content_type = self.environ.get("CONTENT_TYPE")
        if not content_type or "application/json" != content_type:
            response_body = self.handler.get_raw_error(
                self.handler.BadRequestError,
            )
            wsgi_errors.write(str(response_body))
        else:
            response_body = self.handler.handle_raw_request(
                wsgi_input.read(),
                request=self.environ,
            )

        response_headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response_body))),
        ]
        self.start_response("200 OK", response_headers)

        yield response_body

    def head(self) -> WSGIResponse:
        response_headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", "0"),
        ]
        self.start_response("200 OK", response_headers)
        yield b""

    def _not_found(self) -> WSGIResponse:
        response_headers = [
            ("Content-Type", "text/plain"),
            ("Content-Length", "0"),
        ]
        self.start_response("404 Not Found", response_headers)
        yield b""

    def _method_not_allowed(self) -> WSGIResponse:
        response_headers = [
            ("Allow", ", ".join(ALLOWED_METHODS)),
            ("Content-Type", "text/plain"),
            ("Content-Length", "0"),
        ]
        self.start_response("405 Method Not Allowed", response_headers)
        yield b""
