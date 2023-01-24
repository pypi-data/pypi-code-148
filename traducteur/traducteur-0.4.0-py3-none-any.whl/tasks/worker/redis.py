import json
import redis
import time

from typing import Optional

from .base import BaseTaskWorker
from ..task.redis import RedisTask
from ...exceptions.tasks import TaskWorkerException


class RedisTaskWorker(BaseTaskWorker):
    def __init__(self, channel: str, idle_time: int = 1, throws: bool = True, **kwargs) -> None:
        super().__init__()

        self.channel = channel
        self.idle = idle_time
        self.throws = throws

        self.r = redis.Redis(**kwargs)

    def listen(self):
        sub = self.r.pubsub()
        sub.subscribe(self.channel)

        while True:
            message: Optional[str] = sub.get_message()
            if isinstance(message, str):
                message: dict = json.loads(message)
                task: Optional[bytes] = self.r.get(message['id'])
                if isinstance(task, bytes):
                    task: RedisTask = RedisTask.unpickle(task)
                    task.digest()
                elif self.throws:
                    raise TaskWorkerException(f"Got message for new task, but no task found with uuid: {message['id']}!")

            time.sleep(self.idle)