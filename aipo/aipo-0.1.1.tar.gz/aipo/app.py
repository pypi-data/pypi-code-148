import asyncio
from typing import Any, Callable, Dict, Union

from .broker import Broker
from .config import Config
from .events import EventManager
from .task import Task, TaskManager


class AipoApp:
    """Aipo application.

    :param config: Aipo configuration.
        If a string is passed, it's assumed to be a path to a YAML file.
        If a dict is passed, it's assumed to be a dict with the configuration.
    """

    def __init__(self, config: Union[Dict[str, Any], str]) -> None:
        self.config = Config(config)
        self.loop = asyncio.get_event_loop()
        self._broker = Broker(self.loop, self.config)
        self._task_manager = TaskManager(self.loop, self._broker, self)
        self._event_manager = EventManager(["startup", "shutdown", "after_init"], self)

    def task(
        self, func: Callable | None = None, *, queue: str | None = None
    ) -> Callable:
        """Decorator or creating tasks. It can be used with synchronous or
        asynchronous functions.

        :param queue: Which queue instances of this task will be sent to.

        To simply use the default queue, you can use the decorator without arguments:
        .. code-block:: python
            @app.task
            async def foo(arg1, arg2):
                await do_io_stuff(arg1, arg2)

        To use a custom queue, you can use the ``queue`` argument:
        .. code-block:: python
            @app.task(queue='my_queue')
            async def foo(arg1, arg2):
                await do_io_sutff(arg1, arg2)
        """

        def _wrapper(f: Callable) -> Task:
            task = Task(
                func=f,
                queue=queue or self.config.default_queue,
                manager=self._task_manager,
            )
            self._task_manager.bind(task)
            return task

        if func:
            return _wrapper(func)
        return _wrapper

    def on_event(self, event_name: str) -> Callable:
        """Decorator for registering event handlers.

        :param event_name: Name of the event to register the handler for.

        .. code-block:: python
            @app.on_event('startup')
            async def startup():
                print('Aipo is starting up!')
        """

        def _wrapper(func: Callable) -> Callable:
            self._event_manager.register(event_name, func)
            return func

        return _wrapper

    async def start_server(self) -> None:
        await self._event_manager.trigger("startup")
        await self._broker.start()
        await self._task_manager.drain_events()

    async def stop_server(self) -> None:
        self._task_manager.stop_draining_events()
        await self._task_manager.wait()
        await self.close_connections()
        await self._event_manager.trigger("shutdown")

    async def close_connections(self) -> None:
        """Close all connections to the message broker."""
        await self._broker.close()
