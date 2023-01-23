from __future__ import annotations

from aiohttp import web
import asyncio

from pathlib import Path
import importlib
import sys
import os

from typing import List, TYPE_CHECKING
if TYPE_CHECKING:
    from jija.config.base import Config


from jija.collector import collect_subclasses
from jija import middlewares
from jija import commands
from jija import app
from jija import config


class AppGetter(type):
    def __getattr__(self, item):
        """
        :type item: str
        :rtype: App
        """

        jija_app = Apps.apps.get(item)
        if jija_app:
            return jija_app

        raise AttributeError(item)


class Apps(metaclass=AppGetter):
    apps = {}
    commands = {
        'system': commands.COMMANDS
    }

    __REQUIRED_CONFIGS = {
        config.StructureConfig,
        config.DriversConfig,
        config.NetworkConfig
    }

    __INITED_CONFIGS: List[Config] = []
    __PREFLIGHT_TASKS = []

    @classmethod
    def load(cls):
        cls.__init_configs()
        Apps.apps['core'] = cls.__create_base_app()
        cls.__collect(config.StructureConfig.APPS_PATH, Apps.apps['core'])
        cls.__register_apps()

    @classmethod
    def config_init_callback(cls, config_class):
        cls.__INITED_CONFIGS.append(config_class)

    @classmethod
    def __init_configs(cls):
        for config_class in cls.__REQUIRED_CONFIGS:
            if config_class not in cls.__INITED_CONFIGS:
                config_class()

        asyncio.get_event_loop().run_until_complete(cls.__freeze_configs())

    @classmethod
    async def __freeze_configs(cls):
        for config_class in cls.__INITED_CONFIGS:
            await config_class.freeze()
            cls.__PREFLIGHT_TASKS.append(config_class.preflight)

    @classmethod
    def __create_base_app(cls):
        """
        :rtype: web.Application
        """

        aiohttp_app = web.Application()

        aiohttp_app.middlewares.extend([
            middlewares.print_request.PrintRequest(),
        ])

        if cls.app_exists(config.StructureConfig.CORE_PATH):
            app_class = cls.get_modify_class(config.StructureConfig.CORE_PATH)
        else:
            app_class = app.App

        for config_unit in cls.__INITED_CONFIGS:
            aiohttp_app = config_unit.base_app_update(aiohttp_app)

        jija_app = app_class(path=config.StructureConfig.CORE_PATH, aiohttp_app=aiohttp_app, name='core')

        return jija_app

    @staticmethod
    def app_exists(path: Path) -> bool:
        return path.joinpath('app.py').exists()

    @classmethod
    def __collect(cls, path: Path, parent: app.App):
        if not path.exists():
            return

        for sub_app_name in os.listdir(path):
            sub_app_name: str

            next_path = path.joinpath(sub_app_name)
            if app.App.is_app(next_path):
                jija_app = cls.get_modify_class(next_path)(path=next_path, parent=parent, name=sub_app_name)
                cls.commands[sub_app_name] = jija_app.commands
                cls.apps[sub_app_name] = jija_app
                cls.__collect(path.joinpath(sub_app_name), jija_app)

    @staticmethod
    def get_modify_class(path: Path) -> type:
        modify_class_path = path.joinpath('app')
        import_path = ".".join(modify_class_path.relative_to(config.StructureConfig.PROJECT_PATH).parts)

        module = importlib.import_module(import_path)
        modify_class = list(collect_subclasses(module, app.App))
        return modify_class[0] if modify_class else app.App

    @classmethod
    def __register_apps(cls):
        cls.apps['core'].register()

    @classmethod
    def get_command(cls, module, command):
        """
        :type module: str
        :type command: str
        :rtype: type
        """

        if module is None:
            module = 'system'

        return cls.commands[module][command]

    @classmethod
    def run_command(cls):
        args = sys.argv
        command = args[1].split('.')
        Apps.load()
        asyncio.get_event_loop().run_until_complete(cls.__preflight())

        if len(command) == 1:
            module = None
            command = command[0]
        else:
            module, command = command

        command_class = cls.get_command(module, command)
        command_obj = command_class()
        command_obj.run()

    @classmethod
    async def __preflight(cls):
        for task in cls.__PREFLIGHT_TASKS:
            await task()
