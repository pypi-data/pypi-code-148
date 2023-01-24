"""
Authorization service compatible HTTP views and functions.
"""

import asyncio

from aiohttp import web

from kaiju_tools.exceptions import APIException
from kaiju_tools.serialization import dumps
from kaiju_tools.http.views import JSONRPCView
from kaiju_tools.rpc.jsonrpc import InternalError, RPCResponse, RPCError, InvalidParams
from kaiju_tools.rpc.services import JSONRPCServer

from .services import HTTPLoginService

__all__ = (
    'RestrictedJSONRPCView',
)


class RestrictedJSONRPCView(JSONRPCView):
    """
    JSON RPC HTTP view with session based authorization.
    """

    rpc_service_name = JSONRPCServer.service_name
    login_service_name = HTTPLoginService.service_name
    route = '/rpc'

    async def post(self):

        login_service = self.request.app.services[self.login_service_name]

        # a token has a priority over a cookie

        if login_service.has_token(self.request):
            session, body = await asyncio.gather(
                login_service.jwt_get_session(self.request),
                self._get_request_body())
        else:
            if login_service.session_backend_enabled and login_service.user_backend_enabled:
                session, body = await asyncio.gather(
                    login_service.get_session(self.request),
                    self._get_request_body())
            else:
                session = login_service.get_guest_session()
                body = await self._get_request_body()

        if type(body) is dict and body.get('method') in login_service.fake_routes:

            # TODO: возможно есть способ сделать это лучше, чем делать вид, что это RPC
            f = login_service.fake_routes[body.get('method')]
            params = body.get('params', {})
            request_id = body.get('id')
            headers = {}

            try:
                result = f(self.request, **params)
            except (TypeError, AttributeError) as exc:
                data = InvalidParams(request_id, base_exc=exc)
            else:
                try:
                    result = await result
                except APIException as exc:
                    data = RPCError.from_api_exception(id=request_id, exc=exc, debug=self.request.app.debug).repr()
                except Exception as exc:
                    data = InternalError(request_id, base_exc=exc, debug=self.request.app.debug).repr()
                else:
                    data = RPCResponse(request_id, result=result).repr()

        else:
            rpc = self.request.app.services[self.rpc_service_name]
            headers, data = await rpc.call(body, dict(self.request.headers), session=session)

        return web.json_response(data, dumps=dumps, headers=headers, status=200)
