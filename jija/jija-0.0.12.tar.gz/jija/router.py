import typing

from jija import views

from aiohttp import web


class Router:
    def __init__(self, endpoints):
        self.__endpoints = endpoints
        self.__routes = self.__generate_routes(endpoints)

    @property
    def routes(self):
        return self.__routes

    @property
    def endpoints(self):
        return self.__endpoints

    @staticmethod
    def __generate_routes(endpoints):
        result = []
        for endpoint in endpoints:
            result.extend(endpoint.generate_routes())

        return result

    def __repr__(self):
        return f'<{self.__class__.__name__}: {len(self.endpoints)} endpoints, {len(self.__routes)} routes>'

    def __str__(self):
        return self.__repr__()


class AbsEndpoint:
    def generate_routes(self, prefix=''):
        raise NotImplementedError()


class Endpoint(AbsEndpoint):
    def __init__(self, path, view: typing.Type[views.View]):
        if not issubclass(view, views.View):
            raise AttributeError(f'view must be a subclass of "jija.views.View", got {view}')

        self.__path = path
        self.__view = view

    @property
    def path(self) -> str:
        return self.__path

    @property
    def view(self) -> typing.Type[views.View]:
        return self.__view

    def generate_routes(self, prefix=''):
        result = []
        for method in self.__view.get_methods():
            result.append(web.route(method, f'{prefix}{self.__path}', self.__view.construct))

        return result


class Include(AbsEndpoint):
    def __init__(self, path, endpoints):
        if path[-1] == '/':
            raise ValueError('Include path must ends without "/"')

        self.__path = path
        self.__endpoints = endpoints

    @property
    def path(self):
        return self.__path

    @property
    def endpoints(self):
        return self.__endpoints

    def generate_routes(self, prefix=''):
        result = []
        for endpoint in self.__endpoints:
            result.extend(endpoint.generate_routes(f'{self.__path}{prefix}'))

        return result
