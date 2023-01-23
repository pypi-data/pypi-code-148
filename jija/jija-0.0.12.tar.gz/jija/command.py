import asyncio
import inspect


class Command:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def prepare(self):
        pass

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.prepare())

        if inspect.iscoroutinefunction(self.handle):
            self.loop.run_until_complete(self.handle())
        else:
            self.handle()

    def handle(self):
        raise NotImplementedError()
