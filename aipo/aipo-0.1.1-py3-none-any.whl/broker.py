import asyncio
from typing import AsyncIterator, List

from .config import Config
from .message import Message
from .serializers import SerializerBase
from .utils import import_from_string


class Broker:
    """Broker base class.

    Every broker needs to implement the following methods:

    - start
    - close
    - publish
    - subscribe
    - stop_iterator
    - ack
    - is_ready
    """

    def __init__(self, loop: asyncio.AbstractEventLoop, config: Config) -> None:
        self.loop = loop
        self.config = config
        self.serializer: SerializerBase = import_from_string(config.serializer_class)()

    async def start(self) -> None:
        raise NotImplementedError

    async def close(self) -> None:
        raise NotImplementedError

    async def publish(self, msg: Message) -> None:
        raise NotImplementedError

    def subscribe(self, queues: List[str]) -> AsyncIterator[Message]:
        raise NotImplementedError

    def stop_iterator(self) -> None:
        raise NotImplementedError

    async def ack(self, id: str) -> None:
        raise NotImplementedError

    def is_ready(self) -> bool:
        raise NotImplementedError
