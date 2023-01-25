from typing import Any
from typing import Optional
from typing import Union

from drakaina.type_annotations import JSONRPCResponseObject


class RPCError(Exception):
    """Base error class for RPC protocols"""

    def as_dict(self) -> dict[str, str]:
        return {"error": self.__class__.__name__}


class JsonRPCError(RPCError):
    """JSON-RPC Common error

    Reserved for implementation-defined server-errors.
    Codes -32000 to -32099.

    """

    code = -32000
    default_message = "Server error"
    id = None
    data = None

    def __init__(
        self,
        message: str = None,
        details: Optional[Any] = None,
        id_: Union[int, str] = None,
        *args,
        **kwargs,
    ):
        self.id = id_

        if message and details:
            self.data = {"text": message.strip(), "details": details}
        elif message:
            self.data = message.strip()
        elif details:
            self.data = details

        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.code} {self.default_message})"

    def as_dict(self) -> JSONRPCResponseObject:
        error = dict(
            jsonrpc="2.0",
            error={"code": self.code, "message": self.default_message},
            id=self.id,
        )

        if self.data:
            error["error"]["data"] = self.data

        return error


class InvalidRequestError(JsonRPCError):
    """Invalid Request

    The JSON sent is not a valid Request object.

    """

    code = -32600
    default_message = "Invalid Request"


class MethodNotFoundError(JsonRPCError):
    """Method not found

    The method does not exist / is not available.

    """

    code = -32601
    default_message = "Method not found"


class InvalidParamsError(JsonRPCError):
    """Invalid params

    Invalid method parameter(s).

    """

    code = -32602
    default_message = "Invalid params"


class InternalError(JsonRPCError):
    """Internal error

    Internal JSON-RPC error.

    """

    code = -32603
    default_message = "Internal error"


class ParseError(JsonRPCError):
    """Parse error

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.

    """

    code = -32700
    default_message = "Parse error"
