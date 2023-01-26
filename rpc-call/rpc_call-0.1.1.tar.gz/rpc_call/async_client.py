import orjson
import uuid
import asyncio
from aio_pika import connect, Message
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractIncomingMessage,
    AbstractQueue,
)
from typing import MutableMapping
from loguru import logger
from .types import Task, TaskResult


class RPCClient:
    connection: AbstractConnection
    channel: AbstractChannel
    callback_queue: AbstractQueue
    loop: asyncio.AbstractEventLoop

    def __init__(self, amqp_dsn: str, queue_name: str) -> None:
        self.amqp_dsn = amqp_dsn  # RMQ connection string
        self.queue_name = queue_name  # RMQ queue name
        self.futures: MutableMapping[str, asyncio.Future] = {}
        self.loop = asyncio.get_running_loop()

    async def connect(self) -> "RPCClient":
        connection = await connect(self.amqp_dsn)
        self.channel = await connection.channel()
        self.callback_queue = await self.channel.declare_queue(exclusive=True)
        await self.callback_queue.consume(self.on_response)
        return self

    def on_response(self, message: AbstractIncomingMessage) -> None:
        if message.correlation_id is None:
            logger.error(f"Bad message '{message!r}'")
            return
        future: asyncio.Future = self.futures.pop(message.correlation_id)
        future.set_result(message.body)

    async def call(self, task: Task) -> dict:
        correlation_id = str(uuid.uuid4())
        future = self.loop.create_future()
        self.futures[correlation_id] = future
        await self.channel.default_exchange.publish(
            Message(
                orjson.dumps(task.dict()),
                content_type="application/octet-stream",
                correlation_id=correlation_id,
                reply_to=self.callback_queue.name,
            ),
            routing_key=self.queue_name,
        )
        return TaskResult.parse_obj(orjson.loads(await future))
