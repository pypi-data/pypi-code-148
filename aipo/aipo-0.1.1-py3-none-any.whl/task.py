from __future__ import annotations

import asyncio
import logging
import traceback
import uuid
from typing import TYPE_CHECKING, Callable, Dict, Tuple

from .broker import Broker
from .message import Message
from .utils import get_fully_qualified_name

if TYPE_CHECKING:
    from .app import AipoApp

logger = logging.getLogger("aipo")


class Task:
    """A task is a function that can be executed asynchronously.
    It is bound to a queue and a name.
    The name is the fully qualified name of the function.
    The queue is the queue the task is published to.

    :param queue: The queue to publish the task to
    :param func: The function to execute
    :param manager: The task manager that manages this task
    """

    def __init__(
        self,
        *,
        queue: str,
        func: Callable,
        manager: TaskManager,
    ) -> None:
        self._func = func
        self._manager = manager
        self.queue = queue
        self.name = get_fully_qualified_name(func)

    async def execute(self, *args: Tuple, **kwargs: Dict) -> None:
        await self._func(*args, **kwargs)

    async def __call__(self, *args: Tuple, **kwargs: Dict) -> None:
        msg = Message(str(uuid.uuid4()), self.name, tuple(args), kwargs, self.queue)
        await self._manager.publish_task(msg)


class TaskManager:
    """The task manager manages the tasks and executes them.
    It is responsible for publishing task instances to the broker, retrieving and executing.

    :param loop: The event loop to use
    :param broker: The broker to use
    :param app: The app to use
    """

    def __init__(
        self, loop: asyncio.AbstractEventLoop, broker: Broker, app: AipoApp
    ) -> None:
        self._app = app
        self._broker = broker
        self._loop = loop
        self._tasks: Dict[str, Task] = {}
        self._semaphore = asyncio.Semaphore(app.config.max_concurrent_tasks)
        self._running: Dict[asyncio.Future, asyncio.Task] = {}

    def bind(self, task: Task) -> None:
        self._tasks[task.name] = task

    async def publish_task(self, msg: Message) -> None:
        if not self._broker.is_ready():
            await self._broker.start()

        await self._broker.publish(msg)

    async def execute(self, msg: Message) -> None:
        async with self._semaphore:
            future = self._loop.create_future()
            task = self._tasks[msg.name]
            task_instance = asyncio.create_task(self._exec_task(msg, task, future))
            self._running[future] = task_instance

    async def _exec_task(
        self, msg: Message, task: Task, future: asyncio.Future
    ) -> None:
        try:
            start_time = self._loop.time()
            logger.info(f"Executing task {task.name} [{msg.id}]")
            await task.execute(*msg.args, **msg.kwargs)
            await self._broker.ack(msg.id)
            end_time = self._loop.time()
            logger.info(
                f"Task {task.name} [{msg.id}] executed successfully. "
                f"Execution time: {end_time - start_time:.2f} seconds"
            )
        except Exception as exc:
            logger.error(f"Task {task.name} [{msg.id}] raised an exception: {exc}")
            logger.error(traceback.format_exc())
        finally:
            future.set_result(None)
            del self._running[future]

    async def wait(self) -> None:
        if self._running:
            await asyncio.wait(self._running.keys())

    async def drain_events(self) -> None:
        queues = list(set(task.queue for task in self._tasks.values()))
        async for msg in self._broker.subscribe(queues):
            await self.execute(msg)

    def stop_draining_events(self) -> None:
        self._broker.stop_iterator()
