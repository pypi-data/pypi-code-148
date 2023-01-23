import typing
from aiohttp.helpers import sentinel
from aiohttp.typedefs import LooseHeaders
from aiohttp.web import json_response, Response

from jija import serializers


class JsonResponse:
    def __new__(
            cls,
            data: typing.Any = sentinel,
            *,
            text: typing.Optional[str] = None,
            body: typing.Optional[bytes] = None,
            status: int = 200,
            reason: typing.Optional[str] = None,
            headers: typing.Optional[LooseHeaders] = None,
            content_type: str = "application/json"
    ):

        return json_response(
            data=data,
            text=text,
            body=body,
            status=status,
            reason=reason,
            headers=headers,
            content_type=content_type,
        )


class SerializeResponse:
    def __init__(self, data: typing.Any, status: int = 200):
        self.__data = data
        self.__status = status

    @property
    def data(self):
        return self.__data

    @property
    def status(self):
        return self.__status

    async def serialize(self, serializer: serializers.Serializer) -> Response:
        serializer = serializer(data=self.data)
        serialized_data = serializer.serialize_out()

        return json_response(
            body=serialized_data,
            status=self.status,
        )
