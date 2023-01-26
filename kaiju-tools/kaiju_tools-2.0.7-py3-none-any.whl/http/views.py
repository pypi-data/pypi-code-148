import logging
from collections import ChainMap
from typing import *

from aiohttp.web import Response, View
from aiohttp.hdrs import METH_ALL, METH_OPTIONS
from aiohttp.web import json_response
from aiohttp_cors import CorsViewMixin
from rapidjson import JSONDecodeError

from kaiju_tools.exceptions import MethodNotAllowed, JSONParseError
from kaiju_tools.serialization import dumps, loads
from kaiju_tools.rpc.services import JSONRPCServer

__all__ = ('AbstractJSONView', 'AbstractBaseJSONView', 'JSONRPCView')


class AbstractBaseJSONView(CorsViewMixin, View):
    """Base view class."""

    route = None

    async def _get_request_body(self) -> dict:
        try:
            return await self.request.json(loads=loads) if self.request.can_read_body else {}
        except JSONDecodeError as err:
            raise JSONParseError(str(err), json=err.__doc__) from err


class AbstractJSONView(AbstractBaseJSONView):
    """Base view class."""

    route = None
    schema = None
    _methods = None
    _connection = None

    @property
    def connection(self):
        if not self._connection:
            raise AttributeError('No database connection was provided')
        return self._connection

    @property
    def engine(self):
        if not self.request.app.db:
            raise AttributeError('No database connection was provided')
        return self.request.app.db

    @property
    def allowed_methods(self) -> List[str]:
        if self._methods is None:
            methods = [m for m in METH_ALL if hasattr(self, m.lower())]
            self._methods = methods
        return self._methods

    def _get_query_params(self) -> dict:
        query = self.request.query
        q = {}
        for key in query:
            value = query.getall(key)
            if isinstance(value, list) and len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q

    async def _fetch_request_params(self) -> tuple:
        path = self.request.match_info
        body = await self._get_request_body()
        query = self._get_query_params()
        return path, body, query

    @property
    def logger(self):
        if self.request and 'logger' in self.request:
            return self.request['logger']
        else:
            return logging.getLogger(self.__class__.__qualname__)

    def _validate(self, path, body, query) -> ChainMap:
        #
        # if self.schema:
        #     method_lower = self.request.method.lower()
        #     if method_lower in self.schema:
        #         validators = self.schema.get(method_lower)
        #         if 'path' in validators:
        #             self.logger.debug({
        #                 'message': 'валидирует параметры URI',
        #                 'params': path})
        #             try:
        #                 path = validators['path'](path)
        #             except JsonSchemaException as err:
        #                 raise NotFound(
        #                     err.message, url=self.request.url,
        #                     rel_url=self.request.path_qs,
        #                     key=path) from None
        #         try:
        #             if 'body' in validators:
        #                 self.logger.debug({
        #                     'message': 'валидирует параметры тела запроса',
        #                     'params': body})
        #                 _key, _par = 'body', body
        #                 body = validators['body'](body)
        #             if 'query' in validators:
        #                 self.logger.debug({
        #                     'message': 'валидирует параметры query',
        #                     'params': query})
        #                 _key, _par = 'query', query
        #                 query = validators['query'](query)
        #         except JsonSchemaException as err:
        #             raise ValidationError(
        #                 err.message, url=self.request.url,
        #                 rel_url=self.request.path_qs,
        #                 key=_key, value=_par) from err

        return ChainMap(path, body, query)

    async def _iter(self):
        self.logger.debug({'message': 'принимает HTTP запрос', 'method': self.request.method, 'url': self.request.url})
        if self.request.method not in self.allowed_methods:
            self._raise_allowed_methods()
        elif self.request.method == METH_OPTIONS:
            return await super()._iter()
        else:
            params = self._validate(*await self._fetch_request_params())
            method = getattr(self, self.request.method.lower())
            response, headers, status = await method(**params)
            return json_response(response, dumps=dumps, headers=headers, status=status)

    def _raise_allowed_methods(self):
        raise MethodNotAllowed('метод не разрешен', method=self.request.method, allowed_methods=self.allowed_methods)

    def __await__(self):
        return self._iter().__await__()

    def __iter__(self):
        return self._iter().__await__()


class JSONRPCView(AbstractBaseJSONView):
    """A view compatible to the JSON RPC queued server.

    You should bind it to an app router to serve JSON RPC requests.

    .. code-block::python

         app.router.add_view('/rpc', AbstractJSONView)


    A body of each request must be a valid JSON RPC object.
    """

    route = '/public/rpc'
    rpc_service_name = JSONRPCServer.service_name

    async def post(self):
        request = self.request
        if request.can_read_body:
            data = await request.text()
            data = loads(data)
        else:
            data = {}
        rpc = request.app[self.rpc_service_name]
        headers, data = await rpc.call(data, dict(request.headers))
        return Response(text=dumps(data), status=200, headers=headers, content_type='application/json')
