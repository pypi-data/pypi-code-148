import re
import typing

from aiohttp import web
from typing import List, Dict

from jija import views, serializers, router
from jija import apps, app


class DocsProcessor:
    def __init__(self, aiohttp_app: web.Application):
        self.__base_aiohttp_app = aiohttp_app

    async def create_json(self):
        paths = await self.__parse_router('', apps.Apps.core)

        return {
            'openapi': '3.0.1',
            'paths': paths,
        }

    async def __parse_router(self, prefix, jija_app: app.App) -> dict:
        paths = {}

        router_views = self.get_router_views(jija_app.router.endpoints, prefix)

        for path, view in router_views.items():
            path_params = self.parse_path_params(path)
            doc_view = DocView(jija_app.name, view, path_params)
            paths[path] = await doc_view.parse()

        for sub_app in jija_app.childes:
            next_prefix = f'{prefix}/{sub_app.name}'
            paths.update(await self.__parse_router(next_prefix, sub_app))

        return paths

    def get_router_views(
            self,
            endpoints: List[typing.Union[router.Endpoint, router.Include]],
            prefix: str = ''
    ) -> dict:

        router_views = {}
        for endpoint in endpoints:
            if isinstance(endpoint, router.Endpoint):
                if issubclass(endpoint.view, views.DocMixin):
                    router_views[f'{prefix}{endpoint.path}'] = endpoint.view

            elif isinstance(endpoint, router.Include):
                router_views.update(self.get_router_views(endpoint.endpoints, f'{prefix}{endpoint.path}'))

        return router_views

    @staticmethod
    def parse_path_params(path: str) -> Dict[str, serializers.fields.Field]:
        result = {}
        for param in re.findall(r'{(\w*)}', path):
            result[param] = serializers.fields.CharField(required=True)

        return result


class DocView:
    def __init__(
            self,
            app_name,
            view: typing.Type[typing.Union[views.View, views.DocMixin]],
            path_params: Dict[str, serializers.fields.Field]
    ):
        self.__app_name = app_name
        self.__view = view
        self.__path_params = path_params

    async def parse(self):
        methods = {}
        for method in self.__view.get_methods():
            methods[method] = {
                'summary': getattr(self.__view, method).__doc__,
                'tags': [f'{self.__app_name} {self.__view.__name__}'],
                'parameters': self.create_params(self.__path_params, 'path'),

                "responses": {
                    "default": {}
                }
            }

            serializer_in = await self.__view.get_in_serializer(method)

            if serializer_in:
                if method == 'get':
                    methods[method]['parameters'] += self.create_params(serializer_in.get_fields(), 'query')

                else:
                    methods[method]["requestBody"] = self.__parse_serializer_in(serializer_in)

        return methods

    @staticmethod
    def __parse_serializer_in_get(serializer: serializers.Serializer):
        fields = []
        for name, field in serializer.get_fields().items():
            fields.append({
                'name': name,
                'in': 'query',
                'required': field.required,
                "schema": field.doc_get_schema()
            })

        return fields

    @staticmethod
    def __parse_serializer_in(serializer: serializers.Serializer):
        fields = serializer.get_fields()

        required = []
        properties = {}
        for name, field in fields.items():
            if field.required:
                required.append(name)

            properties[name] = field.doc_get_schema()

        return {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "required": required,
                            "properties": properties
                        }
                    }
                }
            }

    @staticmethod
    def create_params(params: Dict[str, serializers.fields.Field], placement: str) -> List[dict]:
        result = []
        for name, field in params.items():
            result.append({
                'name': name,
                'in': placement,
                'required': field.required,
                "schema": field.doc_get_schema()
            })

        return result
