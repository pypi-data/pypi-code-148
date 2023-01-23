import asyncio
import signal
import subprocess

from jija import config
from jija.command import Command
from jija import reloader


class Run(Command):
    def __init__(self):
        super().__init__()
        self.close_event = asyncio.Event()
        self.reloader = reloader.Reloader(config.StructureConfig.PROJECT_PATH, self.close_event)
        self.runner = None

    async def run_watcher(self):
        await self.reloader.wait()

    async def handle(self):
        asyncio.create_task(self.run_watcher())
        while True:
            self.runner = subprocess.Popen([config.StructureConfig.PYTHON_PATH, 'main.py', 'runprocess'])
            self.close_event.clear()
            await self.close_event.wait()
            self.runner.send_signal(signal.SIGINT)
            print()

    def run(self):
        try:
            super().run()
        except KeyboardInterrupt:
            self.reloader.close()
            self.runner.send_signal(signal.SIGINT)
            self.runner.wait()
