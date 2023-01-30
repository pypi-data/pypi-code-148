class BaseJsonRpcException(Exception):
    message = "Unknown exception"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.message)


class JsonRpcRequestIsNotValid(BaseJsonRpcException):
    message = "JSON-RPC request is not valid"


class JsonRpcWrongVersion(BaseJsonRpcException):
    message = "JSON-RPC version MUST be 2.0"


class JsonRpcResponseResultError(BaseJsonRpcException):
    message = "Response is not valid: only one of `error` or `result` should be presented in response"
