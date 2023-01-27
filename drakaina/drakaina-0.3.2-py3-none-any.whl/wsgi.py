from typing import Iterable
from typing import Optional
from typing import Union

from drakaina.config import rpc_config
from drakaina.middlewares.base import BaseMiddleware
from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.rpc_protocols import JsonRPCv2
from drakaina.type_annotations import WSGIApplication
from drakaina.type_annotations import WSGIEnvironment
from drakaina.type_annotations import WSGIErrorsStream
from drakaina.type_annotations import WSGIInputStream
from drakaina.type_annotations import WSGIResponse
from drakaina.type_annotations import WSGIStartResponse

ALLOWED_METHODS = ("OPTIONS", "GET", "POST")


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
        self._rpc_content_type = self.handler.content_type
        self.route = route
        self.provide_smd = provide_smd
        self.provide_openrpc = provide_openrpc
        self.provide_openapi = provide_openapi

        if self.provide_smd or self.provide_openrpc or self.provide_openapi:
            self._allowed_methods = ", ".join(ALLOWED_METHODS)
        else:
            self._allowed_methods = ", ".join(
                [m for m in ALLOWED_METHODS if m != "GET"],
            )

        self._cors_headers = [
            ("Access-Control-Allow-Methods", self._allowed_methods),
            ("Access-Control-Allow-Origin", rpc_config.CORS_ALLOW_ORIGIN),
            ("Access-Control-Allow-Headers", rpc_config.CORS_ALLOW_HEADERS),
            ("Access-Control-Max-Age", "86400"),
        ]

    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        self.environ = environ
        self.start_response = start_response
        method = environ.get("REQUEST_METHOD")

        if self.route:
            path = environ.get("PATH_INFO")
            if path != self.route:
                return self._not_found()

        if method in ALLOWED_METHODS:
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
        content_length = int(self.environ.get("CONTENT_LENGTH"))
        if (
            not (content_type and content_length)
            or content_type != self._rpc_content_type
            or content_length > rpc_config.MAX_CONTENT_SIZE
        ):
            if content_type != self._rpc_content_type:
                response_status = "415 Unsupported Media Type"
            else:
                response_status = "400 Bad Request"
            # Return RPC error
            response_body = self.handler.get_raw_error(
                self.handler.BadRequestError,
            )
            wsgi_errors.write(str(response_body))
        else:
            response_status = "200 OK"
            response_body = self.handler.handle_raw_request(
                wsgi_input.read(),
                request=self.environ,
            )

        response_headers = self._cors_headers + [
            ("Content-Type", self._rpc_content_type),
            ("Content-Length", str(len(response_body))),
        ]
        self.start_response(response_status, response_headers)

        yield response_body

    def options(self) -> WSGIResponse:
        response_headers = self._cors_headers + [
            ("Allow", self._allowed_methods),
            ("Content-Length", "0"),
        ]
        self.start_response("200 OK", response_headers)
        yield b""

    def _not_found(self) -> WSGIResponse:
        response_headers = []
        self.start_response("404 Not Found", response_headers)
        yield b""

    def _method_not_allowed(self) -> WSGIResponse:
        response_headers = [
            ("Allow", self._allowed_methods),
        ]
        self.start_response("405 Method Not Allowed", response_headers)
        yield b""
