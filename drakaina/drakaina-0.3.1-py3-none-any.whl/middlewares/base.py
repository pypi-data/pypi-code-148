from drakaina.type_annotations import ASGIReceive
from drakaina.type_annotations import ASGIScope
from drakaina.type_annotations import ASGISend
from drakaina.type_annotations import WSGIEnvironment
from drakaina.type_annotations import WSGIResponse
from drakaina.type_annotations import WSGIStartResponse


class BaseMiddleware:
    """
    https://peps.python.org/pep-3333/#middleware-handling-of-block-boundaries
    """

    def __init__(self, app, is_async: bool = False):
        self.app = app
        if is_async:
            self.__method = self.__asgi_call__
        else:
            self.__method = self.__wsgi_call__

    def __call__(self, *args, **kwargs):
        return self.__method(*args, **kwargs)

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        return self.app(environ, start_response)

    async def __asgi_call__(self, scope: ASGIScope, receive: ASGIReceive, send: ASGISend):
        return await self.app(scope, receive, send)
