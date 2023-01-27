import abc
import json

from aiohttp import web

from bot_plugin.domain.events import MessageEventRequest


class BasePluginHandler(abc.ABC):
    async def handle_message_event(self, request: web.Request) -> None:
        pass

    async def handle_callback_query_event(self, request: web.Request) -> None:
        pass

    async def _parse_message_event(self, body: str):
        return json.loads(body, object_hook=MessageEventRequest.from_json)


