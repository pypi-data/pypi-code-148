import asyncio
import time
from typing import AsyncIterator, Dict, List

from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
from redis.exceptions import LockNotOwnedError

from ..broker import Broker
from ..config import Config
from ..message import Message


class RedisBroker(Broker):
    """Redis backend broker.
    Implements connection to the Redis server to publish and drain messages.
    """

    unacked_hash = "aipo:unacked_hash"
    unacked_set = "aipo:unacked_set"
    lock_key = "aipo:unacked_lock"

    def __init__(self, loop: asyncio.AbstractEventLoop, config: Config) -> None:
        super().__init__(loop, config)
        self._client: Redis | None = None
        self._stopped = asyncio.Event()
        self._unacked_ttl = config.broker_params.get("unacked_ttl", 1800)
        self._unacked: Dict[str, str] = {}
        self._queues: List[str] = []
        self._curr_fetch: asyncio.Future | None = None

    async def start(self) -> None:
        self.conn_params = self._get_conn_params()
        self._client = Redis(**self.conn_params)
        await self._client.ping()

    def _get_conn_params(self) -> dict:
        conn_params = {
            "host": self.config.broker_params.get("hostname", None),
            "port": self.config.broker_params.get("port", 6379),
            "username": self.config.broker_params.get("username", None),
            "password": self.config.broker_params.get("password", None),
            "max_connections": self.config.broker_params.get("max_connections", 10),
            "socket_timeout": self.config.broker_params.get("socket_timeout", None),
            "socket_connect_timeout": self.config.broker_params.get(
                "socket_connect_timeout", None
            ),
            "socket_keepalive": self.config.broker_params.get("socket_keepalive", None),
            "socket_keepalive_options": self.config.broker_params.get(
                "socket_keepalive_options", None
            ),
            "health_check_interval": self.config.broker_params.get(
                "health_check_interval", 25
            ),
        }
        return conn_params

    async def close(self) -> None:
        if self._client is None:
            return

        self.stop_iterator()
        await self._restore_visibility_task
        await self._restore_unacked()
        await self._client.close()
        self._client = None

    async def publish(self, msg: Message) -> None:
        if self._client is None:
            raise RuntimeError("Redis client is not connected")

        body = self.serializer.encode(
            {
                "id": msg.id,
                "name": msg.name,
                "args": msg.args,
                "kwargs": msg.kwargs,
            }
        )
        await self._client.lpush(msg.queue, body)

    async def ack(self, id: str) -> None:
        if self._client is None:
            raise RuntimeError("Redis client is not connected")

        async with self._client.pipeline(transaction=True) as pipe:
            self._remove_unacked(pipe, id)
            await pipe.execute()
        del self._unacked[id]

    def is_ready(self) -> bool:
        return self._client is not None

    async def _restore_unacked(self) -> None:
        assert self._client is not None

        for id, body in self._unacked.items():
            data = self.serializer.decode(body)
            async with self._client.pipeline(transaction=True) as pipe:
                self._remove_unacked(pipe, id)
                self._republish_unacked(pipe, data["data"], data["queue"])
                await pipe.execute()

    async def _restore_visibility_loop(self) -> None:
        while True:
            await self._restore_visibility()
            try:
                await asyncio.wait_for(self._stopped.wait(), 5 * 60)
            except asyncio.TimeoutError:
                pass
            if self._stopped.is_set():
                break

    async def _restore_visibility(self) -> None:
        assert self._client is not None

        lock = self._client.lock(self.lock_key, timeout=60)
        acquired = await lock.acquire(blocking=False)
        if not acquired:
            return

        try:
            until = time.time() - self._unacked_ttl
            unacked: List[bytes] = await self._client.zrange(
                self.unacked_set, until, 0, byscore=True
            )
            for body in unacked:
                data = self.serializer.decode(body.decode("utf-8"))
                queue = data["queue"]
                msg = self.serializer.decode(data["data"])
                async with self._client.pipeline(transaction=True) as pipe:
                    self._remove_unacked(pipe, msg["id"])
                    self._republish_unacked(pipe, data["data"], queue)
                    await pipe.execute()
        finally:
            try:
                await lock.release()
            except LockNotOwnedError:
                # in case lock timeout
                pass

    def _remove_unacked(self, pipe: Pipeline, id: str) -> None:
        pipe.hdel(self.unacked_hash, id)
        pipe.zrem(self.unacked_set, id)

    def _republish_unacked(self, pipe: Pipeline, data: str, queue: str) -> None:
        pipe.rpush(queue, data)

    async def subscribe(self, queues: List[str]) -> AsyncIterator[Message]:
        self._restore_visibility_task = asyncio.ensure_future(
            self._restore_visibility_loop()
        )
        self._stopped.clear()
        self._queues = queues

        while not self._stopped.is_set():
            self._queue_rotation()
            msg = await self._wait_message()
            if msg:
                yield msg
            else:
                break

    def stop_iterator(self) -> None:
        self._stopped.set()
        if self._curr_fetch:
            self._curr_fetch.cancel()

    def _queue_rotation(self) -> None:
        q = self._queues.pop()
        self._queues.insert(0, q)

    async def _wait_message(self) -> Message | None:
        self._curr_fetch = asyncio.create_task(self._get_message())
        await asyncio.wait(
            [
                self._curr_fetch,
                self._stopped.wait(),
            ],
            return_when=asyncio.FIRST_COMPLETED,
        )
        if self._stopped.is_set():
            return None
        return self._curr_fetch.result()

    async def _get_message(self) -> Message:
        assert self._client is not None

        queue, body = await self._client.brpop(self._queues, timeout=0)
        queue = queue.decode("utf-8")
        body = body.decode("utf-8")
        data = self.serializer.decode(body)
        msg = Message(
            id=data["id"],
            name=data["name"],
            args=data["args"],
            kwargs=data["kwargs"],
            queue=queue,
        )
        await self._add_to_unacked(msg.id, body, queue)
        return msg

    async def _add_to_unacked(self, id: str, data: str, queue: str) -> None:
        assert self._client is not None

        msg = self.serializer.encode({"data": data, "queue": queue})
        async with self._client.pipeline() as pipe:
            pipe.hset(self.unacked_hash, id, msg)
            pipe.zadd(self.unacked_set, {id: time.time()})
            await pipe.execute()
        self._unacked[id] = msg
