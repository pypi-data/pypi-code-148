import inspect
import json
import logging
from dataclasses import is_dataclass

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

from wejr.jsonrpc.errors import request_invalid_error, invalid_params_error
from wejr.jsonrpc.request import Request
from wejr.jsonrpc.response import Response, Error
from wejr.router import Router
from wejr.utils.common import DataclassJsonDictTransformMixin

CHANNEL_MESSAGE_TYPE = "group.message"
logger = logging.getLogger("__name__")


class AsyncBaseJsonRpcConsumer(AsyncJsonWebsocketConsumer):

    client_router: Router
    group_routers: dict[str, Router]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = list(self.group_routers.keys()) if self.group_routers else []

    async def _handle_request(
        self, router: Router, request_raw: dict, from_channel=False
    ):
        """Call callback from command handler, pass data and consumer"""
        error_response = None
        try:
            request = Request.from_dict(request_raw)
        except TypeError:
            error_response = Response(id=None, error=request_invalid_error)
        else:
            handler = await router.get_handler(request.method)
            if handler is None:
                error_response = Response(id=request.id, error=request_invalid_error)
            else:
                handler_parameters = inspect.signature(handler).parameters
                params = request.params or {}
                if parameter := handler_parameters.get("params"):
                    provided_type = parameter.annotation
                    if is_dataclass(provided_type):
                        try:
                            params = provided_type(**params)
                        except TypeError:
                            error_response = Response(
                                id=request.id, error=invalid_params_error
                            )
                    if provided_type not in (dict, inspect.Signature.empty):
                        raise ValueError(
                            f"Invalid annotation for params in handler function, request = {request_raw}"
                        )

                    handler(self, request, params)
                else:
                    handler(self, request)

        if not from_channel and error_response:
            await self.send_jsonrpc_obj(error_response)

    async def receive_json(self, data: dict, **kwargs):
        """Pass websocket data handling to command handler"""
        await self._handle_request(self.client_router, data)

    async def original_dispatch(self, data):
        await super().dispatch(data)

    async def dispatch(self, data):
        """Pass handling group received event to command handler"""
        data_type = data.get("type", "")
        if data_type.startswith("websocket."):
            await self.original_dispatch(data)
        elif data_type == CHANNEL_MESSAGE_TYPE:
            router = self.group_routers.get(data.get("channel", ""))
            if router:
                await self._handle_request(
                    router, data.get("request", {}), from_channel=True
                )
            else:
                # TODO: change log text
                logger.error(f"router for channel not found, data = {data}")
        else:
            await self._handle_request(self.client_router, data)

    async def send_result(self, request: Request, result):
        await self.send_jsonrpc_obj(Response(id=request.id, result=result))

    async def send_error(self, request: Request, error: Error):
        await self.send_jsonrpc_obj(Response(id=request.id, error=error))

    async def send_notification(self, method, params=None):
        await self.send_jsonrpc_obj(Request(method=method, params=params))

    async def send_jsonrpc_obj(self, obj: Request | Response, close=False):
        await self.send_json(obj, close)

    @classmethod
    async def encode_json(cls, content) -> str:
        if isinstance(content, DataclassJsonDictTransformMixin):
            return content.to_json()
        return json.dumps(content)


async def send_to_channel(channel_name: str, method: str, params: dict = None):
    channel_layer = get_channel_layer()
    await channel_layer.group_send(
        channel_name,
        {
            "type": CHANNEL_MESSAGE_TYPE,
            "channel": channel_name,
            "request": Request(method=method, params=params).to_dict(),
        },
    )
