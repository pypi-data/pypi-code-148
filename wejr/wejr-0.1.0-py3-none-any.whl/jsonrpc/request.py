from dataclasses import dataclass, field
from enum import Enum

from wejr.jsonrpc.constants import JSONRPC_VERSION
from wejr.jsonrpc.exceptions import JsonRpcWrongVersion, JsonRpcRequestIsNotValid
from wejr.utils.common import DataclassJsonDictTransformMixin


class JsonRequestType(str, Enum):
    REQUEST = "request"
    TEST_REQUEST = "test_request"
    NOTIFICATION = "notification"


@dataclass
class Request(DataclassJsonDictTransformMixin):
    method: str
    params: dict | None = field(default=None)
    id: str | int | None = field(default=None)
    jsonrpc: str = field(default=JSONRPC_VERSION)

    def __post_init__(self):
        if self.jsonrpc != JSONRPC_VERSION:
            raise JsonRpcWrongVersion

        if not self.method:
            raise JsonRpcRequestIsNotValid("Method cannot be empty string")

        if isinstance(self.id, str) and not self.id:
            raise JsonRpcRequestIsNotValid("Id cannot be empty string")

    @property
    def type(self):
        match self.id:
            case None:
                return JsonRequestType.NOTIFICATION
            case 0:
                return JsonRequestType.TEST_REQUEST
            case _:
                return JsonRequestType.REQUEST
