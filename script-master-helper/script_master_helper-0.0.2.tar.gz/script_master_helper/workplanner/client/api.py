from typing import Any

from aiohttp import ClientResponse, ClientSession
from orjson import orjson

from script_master_helper.workplanner.schemas import ResponseGeneric, Error
from script_master_helper.utils import custom_encoder

_orjson_wrapped = lambda value: orjson.dumps(value, default=custom_encoder).decode()


class ApiError(Exception):
    def __init__(self, response, code, message, detail):
        self.code = code
        self.message = message
        self.detail = detail
        self.response = response

    def __str__(self):
        return f"{self.__class__.__name__}: code={self.code}, message={self.message}, detail={self.detail}, url={self.response.url}"


class AsyncApi:
    def __init__(self, api_root: str, *, headers: dict = None, settings: dict = None):
        self.api_root = api_root
        self.settings = settings or {}
        self.headers = headers or {}

    async def call_endpoint(
        self,
        endpoint,
        method=None,
        params=None,
        headers=None,
        data=None,
        json=None,
    ) -> dict:
        url = self.api_root + endpoint
        self.headers.update(headers or {})

        async with ClientSession(json_serialize=_orjson_wrapped, headers=self.headers) as session:
            async with session.request(method, url, params=params, data=data, json=json, **self.settings) as response:
                return await self.process_response(response)

    async def process_response(self, response: ClientResponse) -> dict:
        data = await self.response_to_native(response)

        if data.error:
            await self.error_handling(response, data.error.code, data.error.message, data.error.detail)

        return data.data

    async def response_to_native(self, response: ClientResponse) -> ResponseGeneric:
        try:
            data = await response.json(loads=orjson.loads, content_type=None)
            return ResponseGeneric(**data)
        except ValueError:
            text = await response.text()
            if response.status != 200:
                return ResponseGeneric(error=Error(message=text, code=response.status))
            else:
                return ResponseGeneric(data=text)

    async def error_handling(self, response: ClientResponse, code: int, message: str, detail: Any):
        raise ApiError(response, code, message, detail)
