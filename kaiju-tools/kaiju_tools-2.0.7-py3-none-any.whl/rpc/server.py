import asyncio
import uuid
import warnings
from contextvars import ContextVar  # noqa
from fnmatch import fnmatch
from time import time
from typing import List, Union, TypedDict, Callable, Dict

import fastjsonschema

from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_tools.rpc.etc import JSONRPCHeaders
from kaiju_tools.rpc.jsonrpc import (
    RPCRequest,
    RPCError,
    RPCResponse,
    RequestTimeout,
    InvalidRequest,
    InvalidParams,
    InternalError,
    AbortedByServer,
    MethodNotFound,
    PermissionDenied,
)
from kaiju_tools.functions import timeout
from kaiju_tools.exceptions import APIException
from kaiju_tools.services import ContextableService, ServiceOfServices
from kaiju_tools.jsonschema import compile_schema

__all__ = ['RequestHeaders', 'RequestContext', 'MethodInfo']


class RequestContext(TypedDict):
    """Request context stored for the request chain."""

    correlation_id: str
    session: dict


REQUEST_CONTEXT: ContextVar[Union[None, RequestContext]] = ContextVar('RequestContext', default=None)


class _Aborted(APIException):
    pass


class RequestHeaders(TypedDict):
    """Request headers acknowledged by the server."""

    correlation_id: str
    request_deadline: int
    abort_on_error: bool


class MethodInfo(TypedDict):
    """Stored method data."""

    f: Callable
    permission: int
    validator: Callable


class JSONRPCServer(ContextableService, ServiceOfServices):
    """A simple JSON RPC interface with method execution and management tasks."""

    service_name = 'rpc'
    _permission_levels = {
        AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION: 0,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_USER_PERMISSION: 100,
        AbstractRPCCompatible.PermissionKeys.GLOBAL_GUEST_PERMISSION: 1000,
    }

    def __init__(
        self,
        app,
        *,
        max_parallel_tasks: int = 128,
        default_request_time: int = 120,
        max_request_time: int = 600,
        enable_permissions: bool = True,
        logger=None,
    ):
        """Initialize.

        :param app: web app
        :param max_parallel_tasks: max number of tasks in the loop
        :param default_request_time: (s)
        :param max_request_time: (s)
        :param enable_permissions: enable perm checks in requests
        :param logger:
        """
        ContextableService.__init__(self, app=app, logger=logger)
        self._max_parallel_tasks = max(1, int(max_parallel_tasks))
        self._default_request_time = max(1, int(default_request_time))
        self._max_request_time = max(self._default_request_time, int(max_request_time))
        self._enable_permissions = enable_permissions
        self._debug = self.app.debug
        self._counter = self._max_parallel_tasks
        self._not_full = asyncio.Event()
        self._not_full.set()
        self._empty = asyncio.Event()
        self._empty.set()
        self._methods: Dict[str, MethodInfo] = {}

    async def init(self):
        self.app.get_session = self.get_session
        self.logger.info('Starting.')
        if not self._enable_permissions:
            warnings.warn('Server permissions are disabled.')
        self._counter = self._max_parallel_tasks
        self._empty.set()
        self._not_full.set()
        await super().init()

    @staticmethod
    def get_session() -> Union[AbstractRPCCompatible.ServerSessionFlag, object]:
        ctx = REQUEST_CONTEXT.get()
        if ctx is None:
            return AbstractRPCCompatible.ServerSessionFlag
        return ctx['session']

    async def close(self):
        await self._empty.wait()
        await super().close()

    def register_service(self, service_name: str, service: AbstractRPCCompatible) -> None:
        """Register an RPC compatible service and its methods."""
        if not isinstance(service, AbstractRPCCompatible):
            raise TypeError('Service must be rpc compatible.')
        permissions = service.permissions
        validators = service.validators
        for route, f in service.routes.items():
            full_name = f'{service_name}.{route}'
            validator = validators.get(route, None)
            for pattern, perm in permissions.items():
                if fnmatch(route, pattern):
                    break
            else:
                perm = AbstractRPCCompatible.PermissionKeys.GLOBAL_SYSTEM_PERMISSION
            if validator:
                validator = compile_schema(validator)
            method = MethodInfo(f=f, permission=self._permission_levels[perm], validator=validator)
            self._methods[full_name] = method

    async def call(
        self,
        body: Union[List, Dict],
        headers: dict = None,
        session=AbstractRPCCompatible.ServerSessionFlag,
        nowait: bool = False,
    ) -> asyncio.Task:
        """Call a server command.

        :param body: request body
        :param headers: request headers (optional)
        :param session: client session object
        :param nowait: do not wait for the result
        """
        headers = self._get_request_headers(headers)
        if type(body) in {list, tuple}:
            coro = self._execute_batch(
                body,
                request_deadline=headers['request_deadline'],
                abort_on_error=headers['abort_on_error'],
                session=session,
                correlation_id=headers['correlation_id'],
            )
        else:
            coro = self._execute_single(
                body,
                request_deadline=headers['request_deadline'],
                session=session,
                correlation_id=headers['correlation_id'],
            )
        self._counter -= 1
        if not self._not_full.is_set():
            await self._not_full.wait()
        task = asyncio.create_task(coro)
        task.add_done_callback(self._request_done_cb)
        if self._empty.is_set():
            self._empty.clear()
        if self._counter == 0:
            self._not_full.clear()
        if nowait:
            return task
        else:
            result = await task
            return {JSONRPCHeaders.CORRELATION_ID_HEADER: headers['correlation_id']}, result  # noqa compatibility

    @staticmethod
    def _parse_number_value(value, min_val, max_val, default) -> int:
        if not value:
            return default
        try:
            value = int(value)
        except Exception:  # noqa
            return default
        return min(max(min_val, value), max_val)

    @staticmethod
    def _parse_boolean_value(value, default) -> bool:
        if not value:
            return default
        return value.lower() == 'true'

    def _get_request_headers(self, headers: Union[dict, None]) -> RequestHeaders:
        if headers is None:
            headers = {}
        request_deadline = headers.get(JSONRPCHeaders.REQUEST_DEADLINE_HEADER)
        t0 = int(time())
        if request_deadline:
            request_deadline = self._parse_number_value(request_deadline, 0, t0 + self._max_request_time, 0)
        else:
            request_timeout = self._parse_number_value(
                headers.get(JSONRPCHeaders.REQUEST_TIMEOUT_HEADER),
                1,
                self._max_request_time,
                self._default_request_time,
            )
            request_deadline = t0 + request_timeout + 1
        return RequestHeaders(
            correlation_id=headers.get(JSONRPCHeaders.CORRELATION_ID_HEADER, str(uuid.uuid4())),
            request_deadline=request_deadline,
            abort_on_error=self._parse_boolean_value(headers.get(JSONRPCHeaders.ABORT_ON_ERROR), False),
        )

    async def _execute_single(
        self, body, request_deadline: int, session, correlation_id
    ) -> Union[RPCResponse, RPCError]:
        REQUEST_CONTEXT.set(RequestContext(session=session, correlation_id=correlation_id))
        try:
            async with timeout(request_deadline - time()):
                return await self._execute_request(body)
        except asyncio.TimeoutError:
            return RequestTimeout()

    async def _execute_batch(
        self, request: List[dict], request_deadline: int, abort_on_error: bool, session, correlation_id
    ) -> List[Union[RPCResponse, RPCError]]:
        """Execute multiple coroutine functions."""
        results = []
        REQUEST_CONTEXT.set(RequestContext(session=session, correlation_id=correlation_id))
        for n, row in enumerate(request):
            try:
                async with timeout(request_deadline - time()):
                    result = await self._execute_request(row, id_=n)
                    if abort_on_error and isinstance(result, RPCError):
                        raise _Aborted
            except _Aborted:
                results.extend((AbortedByServer(id=id_) for id_ in range(n + 1, len(request) + 1)))
                return results
            except asyncio.TimeoutError:
                results.extend((RequestTimeout(id=id_) for id_ in range(n + 1, len(request) + 1)))
                return results
            else:
                results.append(result)
        return results

    async def _execute_request(self, request: dict, id_=0) -> Union[RPCResponse, RPCError]:
        if type(request) is not dict:
            raise InvalidRequest(id=id_, message='Request body must be a JSONRPC object.')
        if 'id' not in request:
            request['id'] = id_
        try:
            request = RPCRequest(**request)
            id_ = request.id
        except Exception as exc:
            return InvalidRequest(id=id_, base_exc=exc, debug=self._debug, message=str(exc))
        if request.params is None:
            params = {}
        elif type(request.params) is dict:
            params = request.params
        else:
            return InvalidParams(id=id_, message='Request params must be either a mapping or null.')
        try:
            method = self._methods[request.method]
        except KeyError:
            return MethodNotFound(id=id_, data={'method': request.method})
        if method['validator']:
            try:
                params = method['validator'](params)
            except fastjsonschema.JsonSchemaException as exc:
                return InvalidParams(id=id_, message=str(exc), base_exc=exc)
        if self._enable_permissions:
            user_scope = 0
            permissions = set()
            if method['permission'] < user_scope and request.method not in permissions:
                return PermissionDenied(id=id_, data={'method': request.method})
        try:
            coro = method['f'](**params)
        except Exception as exc:
            return InvalidParams(id=request.id, base_exc=exc, message=str(exc))
        try:
            result = await coro
            return RPCResponse(id=id_, result=result)
        except asyncio.TimeoutError:
            return RequestTimeout(id=id_)
        except APIException as exc:
            return RPCError.from_api_exception(id_, exc, debug=self._debug)
        except Exception as exc:
            self.logger.info('RPC error.', exc_info=exc)
            return InternalError(id=id_, base_exc=exc, debug=self._debug)

    def _request_done_cb(self, task: asyncio.Task) -> None:
        """Increment the counter when a request is finished."""
        self._counter += 1
        if self._counter >= self._max_parallel_tasks:
            self._counter = self._max_parallel_tasks
            self._empty.set()
        if not self._not_full.is_set():
            self._not_full.set()
        exc = task.exception()
        if exc:
            self.logger.error('Execution error: {task_name}', exc_info=exc)
