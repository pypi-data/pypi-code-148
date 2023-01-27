import asyncio
from typing import Optional, Callable
from threading import Event
from tmktprocess import Process


class AsyncProcess(Process):

    def __init__(self, async_func: Callable, event_callback: Optional[Event] = None):
        self._async_func = async_func
        Process.__init__(self, self.__wrapper, event_callback)

    def __wrapper(self, *args, **kwargs) -> None:
        """
        Wrap your async function in an event loop
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self._async_func(*args, **kwargs))
