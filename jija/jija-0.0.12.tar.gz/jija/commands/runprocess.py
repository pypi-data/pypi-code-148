from aiohttp import web
from jija.command import Command


class RunProcess(Command):
    def handle(self):
        from jija.apps import Apps
        from jija.config import NetworkConfig

        web.run_app(Apps.core.aiohttp_app, loop=self.loop, host=NetworkConfig.HOST, port=NetworkConfig.PORT)
