from dataclasses import dataclass, field

from wejr.jsonrpc.constants import JSONRPC_VERSION
from wejr.jsonrpc.exceptions import JsonRpcResponseResultError, JsonRpcWrongVersion
from wejr.utils.common import DataclassJsonDictTransformMixin


@dataclass
class Error:
    code: int
    message: str
    data: dict | None = field(default=None)


@dataclass
class Response(DataclassJsonDictTransformMixin):
    id: str | int | None = field(default=None)
    result: any = field(default=None)
    error: Error | None = field(default=None)
    jsonrpc: str = field(default=JSONRPC_VERSION)

    def __post_init__(self):
        if self.jsonrpc != JSONRPC_VERSION:
            raise JsonRpcWrongVersion

        if bool(self.result) is bool(self.error):
            raise JsonRpcResponseResultError
