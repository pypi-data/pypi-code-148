import logging
from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from drakaina import rpc_registry
from drakaina.exceptions import InternalError
from drakaina.exceptions import InvalidRequestError
from drakaina.exceptions import MethodNotFoundError
from drakaina.exceptions import ParseError
from drakaina.exceptions import RPCError
from drakaina.registries import RPCRegistry
from drakaina.serializers import BaseSerializer
from drakaina.type_annotations import JSONRPCRequest
from drakaina.type_annotations import JSONRPCRequestObject
from drakaina.type_annotations import JSONRPCResponse
from drakaina.type_annotations import JSONRPCResponseObject

__all__ = ("BaseRPCProtocol", "JsonRPCv2")

log = logging.getLogger(__name__)


class BaseRPCProtocol:

    registry: RPCRegistry
    serializer: BaseSerializer

    BadRequestError = RPCError
    InternalError = RPCError
    ParseError = RPCError

    def __init__(
        self,
        registry: RPCRegistry = None,
        serializer: BaseSerializer = None,
    ):
        self.registry = registry
        if registry is None:
            self.registry = rpc_registry
        self.serializer = serializer

    def handle_raw_request(
        self,
        raw_data: bytes,
        request: Optional[Any] = None,
    ) -> bytes:
        try:
            parsed_data = self.serializer.deserialize(raw_data)
        except RPCError as error:
            return self.serializer.serialize(error.as_dict())
        except Exception:
            return self.serializer.serialize(self.ParseError().as_dict())

        response_data = self.handle(parsed_data, request=request)

        try:
            raw_response_data = self.serializer.serialize(response_data)
        except RPCError as error:
            return self.serializer.serialize(error.as_dict())
        except Exception:
            return self.serializer.serialize(self.InternalError().as_dict())

        return raw_response_data

    def get_raw_error(self, error: Union[RPCError, Type[RPCError]]) -> bytes:
        if isinstance(error, type) and issubclass(error, RPCError):
            error = error()
        else:
            assert isinstance(error, RPCError)
        return self.serializer.serialize(error.as_dict())

    def handle(self, rpc_request: Any, request: Optional[Any] = None) -> Any:
        raise NotImplementedError

    @property
    def content_type(self) -> str:
        return self.serializer.content_type

    def smd_scheme(self) -> bytes:
        raise NotImplementedError

    def openrpc_scheme(self) -> bytes:
        raise NotImplementedError

    def openapi_scheme(self) -> bytes:
        raise NotImplementedError


class JsonRPCv2(BaseRPCProtocol):
    """JSON-RPC 2.0 implementation"""

    BadRequestError = InvalidRequestError
    InternalError = InternalError
    ParseError = ParseError

    def handle(
        self,
        rpc_request: JSONRPCRequest,
        request: Optional[Any] = None,
    ) -> JSONRPCResponse:
        """Handles a procedure call or batch of procedure call

        :param rpc_request: RPC request in protocol format.
        :type rpc_request: JSONRPCRequest
        :param request: Optional parameter that can be passed as an
                        argument to the procedure.
        :type request: Any
        :return: Returns the result in protocol format.
        :rtype: JSONRPCResponse
        """
        # Check bad request
        if not (isinstance(rpc_request, (dict, list)) and len(rpc_request) > 0):
            return InvalidRequestError().as_dict()

        # Handle batch request
        if isinstance(rpc_request, list):
            batch_result = []
            for request_object in rpc_request:
                result = self.execute(request_object, request=request)
                if result is not None:
                    batch_result.append(result)
            return batch_result

        # Handle single request
        return self.execute(rpc_request, request=request)

    def execute(
        self,
        procedure_call: JSONRPCRequestObject,
        request: Optional[Any] = None,
    ) -> Optional[JSONRPCResponseObject]:
        """Execute a remote procedure call.

        :param procedure_call: RPC request object in protocol format.
        :type procedure_call: JSONRPCRequestObject
        :param request: Optional parameter that can be passed as an
                        argument to the procedure.
        :type request: Any
        :return: Returns a result object in protocol format.
        :rtype: JSONRPCResponseObject
        """
        method: str = procedure_call.get("method")
        params: Optional[Union[list, dict]] = procedure_call.get("params")
        request_id: Optional[Union[int, str]] = procedure_call.get("id")

        # Validate protocol
        if (
            procedure_call.get("jsonrpc") != "2.0"
            or not isinstance(method, str)
            or not (params is None or isinstance(params, (list, dict)))
            or not (request_id is None or isinstance(request_id, (int, str)))
        ):
            return InvalidRequestError(id=request_id).as_dict()

        # Getting procedure
        procedure = self.registry[method]
        if procedure is None:
            return MethodNotFoundError(id=request_id).as_dict()

        # Prepare parameters
        args, kwargs = [], {}
        if getattr(procedure, "__rpc_provide_request", False):
            kwargs.update(request=request)
        if params and isinstance(params, list):
            args = params
        elif params and isinstance(params, dict):
            kwargs.update(params)

        # Execute RPC method
        try:
            result = procedure(*args, **kwargs)
        except Exception as err:
            return InternalError(message=str(err), id_=request_id).as_dict()

        if request_id is None:
            return None

        return dict(jsonrpc="2.0", result=result, id=request_id)
