import asyncio
from threading import Thread


class AsyncThreader:

    def __init__(self, func):
        self._target = func

    def __wrapper(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._target(*args, **kwargs))

    def __call__(self, *args, **kwargs):
        t = Thread(target=self.__wrapper, args=args, kwargs=kwargs)
        t.start()
        return t
