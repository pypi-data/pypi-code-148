from typing import AsyncIterator, Any

from aiohttp import ClientResponse, ClientSession, ClientError
from orjson import orjson

from script_master_helper.executor.schemas import ResponseGenericSchema, Error

_orjson_wrapped = lambda value: orjson.dumps(value).decode()


class ApiError(ClientError):
    def __init__(self, response, code, message):
        self.code = code
        self.message = message
        self.response = response

    def __repr__(self):
        return f"{self.__class__.__name__}: code={self.code}, message={self.message}, url={self.response.url}"

    def __str__(self):
        return f"{self.__class__.__name__}: code={self.code}, message={self.message}"

    def __eq__(self, other):
        return other.code == self.code and other.message == self.message


class AsyncApi:
    def __init__(self, api_root: str, *, headers: dict = None, settings: dict = None):
        self.api_root = api_root
        self.settings = settings or {}
        self.headers = headers or {}

    async def call_endpoint(
        self,
        method,
        endpoint,
        *,
        params=None,
        headers=None,
        data=None,
        json=None,
    ) -> Any:
        url = self.api_root + endpoint

        async with ClientSession(json_serialize=_orjson_wrapped, headers=self.headers | (headers or {})) as session:
            async with session.request(method, url, params=params, data=data, json=json, **self.settings) as response:
                return await self.process_response(response)

    async def stream_endpoint(
        self,
        method,
        endpoint,
        *,
        params=None,
        headers=None,
        data=None,
        json=None,
    ) -> AsyncIterator[Any]:
        url = self.api_root + endpoint

        async with ClientSession(json_serialize=_orjson_wrapped, headers=self.headers | (headers or {})) as session:
            async with session.request(method, url, params=params, data=data, json=json, **self.settings) as response:
                if response.status != 200:
                    await self.process_response(response)

                async for chunk in response.content:
                    yield chunk

    async def process_response(self, response: ClientResponse) -> Any:
        data = await self.response_to_native(response)

        if data.error:
            await self.process_error(response, data.error.code, data.error.message)

        return data.data

    async def response_to_native(self, response: ClientResponse) -> ResponseGenericSchema:
        try:
            data = await response.json(loads=orjson.loads, content_type=None)
            return ResponseGenericSchema(**data)
        except ValueError:
            text = await response.text()
            if response.status != 200:
                return ResponseGenericSchema(error=Error(message=text, code=response.status))
            else:
                return ResponseGenericSchema(data=text)

    async def process_error(self, response: ClientResponse, code: int, message: str):
        raise ApiError(response, code, message)
