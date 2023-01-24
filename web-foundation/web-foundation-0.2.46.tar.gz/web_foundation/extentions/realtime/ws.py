from dataclasses import dataclass, field
from typing import Any, Coroutine, Callable

import loguru
from sanic.server.websockets.impl import WebsocketImplProtocol

from web_foundation.extentions.realtime.connection import WriteableObj, RtConnection, RtEventCallback, RtMessage
from web_foundation.extentions.request_handler import InputContext


@dataclass
class WSRtMessage(RtMessage):
    msg: str = field(default="")

    def _prepare(self, *args, **kwargs) -> str | bytes:
        return self.msg


class WriteableWs(WriteableObj):
    obj: WebsocketImplProtocol

    def __init__(self, obj: WebsocketImplProtocol):
        super().__init__(obj)

    async def write(self, message: str) -> None:
        await self.obj.send(message)


ReadCallback = Callable[[RtConnection, str], Coroutine[Any, Any, RtMessage | None]]

class WsRtConnection(RtConnection):
    read_callback: ReadCallback

    def __init__(self, input_ctx: InputContext, writeable: WriteableObj, resolve_callback: RtEventCallback,
                 read_callback: ReadCallback = None):
        super().__init__(input_ctx, writeable, resolve_callback, ping_enable=False)
        self.read_callback = read_callback

    async def freeze_request(self, on_disconnect: Callable[[], Coroutine]):
        self._on_disconnect = on_disconnect
        if self.read_callback:
            async for msg in self.writeable.obj:
                await self.read_callback(self, msg)

    @classmethod
    async def accept_connection(cls, input_ctx: InputContext,
                                resolve_callback: RtEventCallback = None,
                                read_callback: ReadCallback = None
                                ):
        async with cls(
                input_ctx=input_ctx,
                writeable=await cls._construct_writable(input_ctx),
                resolve_callback=resolve_callback,
                read_callback=read_callback
        ) as connection:
            await input_ctx.request.app.ctx.rt_broadcaster.accept_rt_connection(
                conn=connection
            )

    @classmethod
    async def _construct_writable(cls, input_ctx: InputContext, *args, **kwargs) -> WriteableWs:
        ws_conn = input_ctx.r_kwargs.pop('ws', None)
        if not ws_conn:
            loguru.logger.error(f"Haven't WS connection in input ctx")
        return WriteableWs(ws_conn)
