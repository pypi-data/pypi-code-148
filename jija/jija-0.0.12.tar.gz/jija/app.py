import importlib
import os
from pathlib import Path

from aiohttp import web
from jija import config

from jija.middleware import Middleware
from jija.collector import collect_subclasses
from jija.command import Command
from jija import router


class App:
    def __init__(self, *, name, path, aiohttp_app=None, parent=None):
        """
        :type name: str
        :type path: jija.utils.path.Path
        :type aiohttp_app: web.Application
        :type parent: App
        """

        self.__parent = parent
        if parent:
            parent.add_child(self)

        self.__path = path
        self.__name = name
        self.__is_core = aiohttp_app is not None

        self.__router = None
        self.__middlewares = None
        self.__commands = None

        self.__aiohttp_app = None

        self.__childes = []
        self.__load(aiohttp_app)

    @property
    def parent(self):
        """:rtype: App"""
        return self.__parent

    @property
    def name(self):
        """:rtype: str"""
        return self.__name

    @property
    def router(self) -> router.Router:
        return self.__router

    @property
    def middlewares(self):
        """:rtype: list[Middleware]"""
        return self.__middlewares

    @property
    def aiohttp_app(self):
        """:rtype: web.Application"""
        return self.__aiohttp_app

    @property
    def childes(self):
        """:rtype: list[App]"""
        return self.__childes

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def commands(self) -> list:
        return self.__commands

    def __load(self, aiohttp_app: web.Application = None):
        self.__router = self.__get_router()
        self.__middlewares = self.__get_middlewares()
        self.__commands = self.__get_commands()

        self.__aiohttp_app = self.get_aiohttp_app(aiohttp_app)

    def __get_router(self) -> "router.Router":
        if not self.exist('routes'):
            raw_routes = []

        else:
            import_path = self.get_import_path('routes')
            routes_module = importlib.import_module(import_path)

            raw_routes = getattr(routes_module, 'routes', [])

        app_router = router.Router(raw_routes)
        return app_router

    def __get_middlewares(self) -> list:
        if not self.exist('middlewares'):
            return []

        import_path = self.get_import_path('middlewares')
        middlewares_module = importlib.import_module(import_path)
        middlewares = collect_subclasses(middlewares_module, Middleware)

        return list(map(lambda middleware: middleware(), middlewares))

    def __get_commands(self) -> dict:
        if not self.exist('commands'):
            return {}

        commands = {}
        commands_path = self.__path.joinpath('commands')
        for file in os.listdir(commands_path):
            if file.endswith('.py') and not file.startswith('_'):

                import_path = self.get_import_path(f'commands.{file.removesuffix(".py")}')
                command_module = importlib.import_module(import_path)

                command = list(collect_subclasses(command_module, Command))
                if command:
                    commands[file.replace('.py', '')] = command[0]

        return commands

    @staticmethod
    def is_app(path: Path) -> bool:
        if not path.is_dir() or not path.joinpath('app.py').exists():
            return False

        for part in path.parts:
            if part.startswith('__'):
                return False

        return True

    def get_aiohttp_app(self, aiohttp_app: web.Application = None) -> web.Application:
        aiohttp_app = aiohttp_app or web.Application()

        aiohttp_app.middlewares.extend(self.__middlewares)

        aiohttp_app.add_routes(self.__router.routes)
        aiohttp_app['JIJA_ROUTER'] = self.__router

        return aiohttp_app

    def add_child(self, child: "App"):
        self.__childes.append(child)

    def get_import_path(self, to: str) -> str:
        modify_class_path = self.path.joinpath(to)
        return ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

    def exist(self, name: str) -> bool:
        return os.path.exists(f'/{self.__path}/{name}') or os.path.exists(f'/{self.__path}/{name}.py')

    def register(self):
        for child in self.childes:
            child.register()
            self.aiohttp_app.add_subapp(prefix=f'/{child.name}', subapp=child.aiohttp_app)
