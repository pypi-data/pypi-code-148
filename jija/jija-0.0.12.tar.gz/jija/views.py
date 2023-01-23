import json

from aiohttp import web

from jija import response, serializers, exceptions


class View:
    methods = ('get', 'post', 'patch', 'put', 'delete')

    serializers_in = None
    # serializers_out = None TODO

    def __init__(self, request: web.Request, path_params: web.UrlMappingMatchInfo):
        self.__method = request.method.lower()
        self.__data: dict = {}
        self.__request = request
        self.__path_params = path_params

    @property
    def method(self) -> str:
        return self.__method

    @property
    def request(self) -> web.Request:
        return self.__request

    @property
    def data(self) -> dict:
        return self.__data

    @classmethod
    def get_methods(cls):
        view_methods = []
        for method in cls.methods:
            if hasattr(cls, method):
                view_methods.append(method)

        return view_methods

    @classmethod
    async def construct(cls, request: web.Request):
        view = cls(request, request.match_info)
        return await view.wrapper()

    async def wrapper(self):
        try:
            return await self.dispatch()

        except exceptions.ViewForceExit as exception:
            return exception.response

    async def dispatch(self):
        try:
            await self.load_data()
            handler = getattr(self, self.method)
            return await handler()
        except serializers.SerializeError as error:
            return response.JsonResponse(error.serializer.errors, status=400)

    async def load_data(self):
        data = {
            **await self.parse_body(),
            **self.parse_path(),
            **self.parse_query()
        }

        self.__data = await self.in_serialize(data)

    async def parse_body(self) -> dict:
        if self.method != 'get':
            try:
                return await self.request.json()
            except json.JSONDecodeError:
                return {}

        return {}

    def parse_path(self) -> dict:
        return dict(self.request.match_info)

    def parse_query(self) -> dict:
        data = {}

        for key in set(self.request.query.keys()):
            value = self.request.query.getall(key)
            if len(value) == 1:
                value = value[0]

            data[key] = value

        return data

    async def in_serialize(self, data: dict) -> dict:
        serializer_class = await self.get_in_serializer(self.method)
        if serializer_class:
            serializer = serializer_class(data)
            await serializer.in_serialize()

            if not serializer.valid:
                raise serializers.SerializeError(serializer)

            return serializer.data

        return data

    async def out_serialize(self, response) -> web.Response:
        # if isinstance(response, SerializeResponse): TODO
        #
        #     serializer_class = await self.get_out_serializer(self.method)
        #     if not serializer_class:
        #         raise ValueError('Got SerializerResponse, but out serializer not set')
        #
        #     return await response.serialize(serializer_class)

        return response

    @classmethod
    async def get_in_serializer(cls, method):
        return cls.serializers_in and cls.serializers_in[method]

    # @classmethod TODO
    # async def get_out_serializer(cls, method):
    #     return cls.serializers_out and cls.serializers_out[method]


class SerializersSet:
    def __init__(self, get=None, post=None, put=None, path=None, delete=None, **kwargs):
        self.__serializers = {
            'get': get,
            'post': post,
            'put': put,
            'path': path,
            'delete': delete,
            **kwargs
        }

    def __getitem__(self, item):
        return self.__serializers[item]


class DocMixin:
    pass
