import asyncio
import time
import uuid
import traceback
from typing import Awaitable, Dict
from hedra.core.engines.types.common.timeouts import Timeouts
from hedra.core.engines.types.common.concurrency import Semaphore
from hedra.core.engines.types.common.base_result import BaseResult
from hedra.core.graphs.simple_context import SimpleContext
from .task import Task
from .result import TaskResult


class MercuryTaskRunner:

    __slots__ = (
        'pool',
        'session_id',
        'timeouts',
        'concurrency',
        'registered',
        'sem',
        'active',
        'waiter',
        'closed'
    )

    def __init__(self, concurrency: int=10**3, timeouts: Timeouts = Timeouts()) -> None:
        
        self.session_id = str(uuid.uuid4())

        self.timeouts = timeouts
        self.concurrency = concurrency

        self.registered: Dict[str, Task] = {}
        self.closed = False
        self.pool = SimpleContext()
        self.pool.size = concurrency
        self.pool.reset_connections = False
        self.pool.create_pool = lambda: None

        self.sem = asyncio.Semaphore(value=concurrency)
        self.active = 0
        self.waiter = None

    async def wait_for_active_threshold(self):
        if self.waiter is None:
            self.waiter = asyncio.get_event_loop().create_future()
            await self.waiter

    def extend_pool(self, increased_capacity: int):
        self.concurrency += increased_capacity
        self.sem = Semaphore(self.concurrency)

    def shrink_pool(self, decrease_capacity: int):
        self.concurrency -= decrease_capacity
        self.sem = Semaphore(self.concurrency)

    async def execute_prepared_request(self, task: Task) -> Awaitable[TaskResult]:

        result = None
        wait_start = time.monotonic()
        self.active += 1

        task_event = task.event
 
        async with self.sem:
            
            try:

                if task.hooks.listen:
                    event = asyncio.Event()
                    task.hooks.channel_events.append(event)
                    await event.wait()
                

                if task_event:
                    await task_event.execute_pre()

                start = time.monotonic()

                result: BaseResult = await task.execute()
                
                result.name = task.name
                result.source = task.source
                result.user = task.metadata.user
                result.tags = task.metadata.tags
                result.checks = task.hooks.checks
                result.wait_start = wait_start
                result.start = start
                result.complete = time.monotonic()


                if task_event:
                    task = await task_event.execute_post(task)

                if task.hooks.notify:
                    await asyncio.gather(*[
                        asyncio.create_task(
                            channel.call(result, task.hooks.listeners)
                        ) for channel in task.hooks.channels
                    ])

                    for listener in task.hooks.listeners: 
                        if len(listener.hooks.channel_events) > 0:
                            event = listener.hooks.channel_events.pop()
                            if not event.is_set():
                                event.set()   

            except Exception as e:
                result = TaskResult(task)

                result.wait_start = wait_start
                result.start = start
                result.complete = time.monotonic()
                result.error = str(e)

            self.active -= 1
            if self.waiter and self.active <= self.concurrency:

                try:
                    self.waiter.set_result(None)
                    self.waiter = None

                except asyncio.InvalidStateError:
                    self.waiter = None

            return result

    async def close(self):
        pass
