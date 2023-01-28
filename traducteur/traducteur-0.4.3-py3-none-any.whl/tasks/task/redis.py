import json
from typing import Optional

import dill as pickle
from ..base import BaseTask
from ...models.document import BaseRedisModel


class RedisTask(BaseTask, BaseRedisModel):
    channel: str

    def queue(self, **kwargs):
        self._queue_children()

        super().queue(**kwargs)

        r = self.redis_instance()

        task: bytes = pickle.dumps(self)
        r.set(self.id, task)

        # no parent => start
        if not self.has_parent:
            self._publish()

    def digest(self):
        r = self.redis_instance()

        # if self has parent => override tin with parents tout
        if self.has_parent:
            parent: bytes = r.get(self.parent)
            parent: BaseTask = self.unpickle(parent)
            self.tin = parent.tout

        # exec
        super().digest()

        # update task status
        task: bytes = pickle.dumps(self)
        r.set(self.id, task)

        if self.has_children:
            # exec children
            for child_id in self.children:
                self._publish(child_id)
        
    def _publish(self, uuid: Optional[str] = None):
        r = self.redis_instance()
        message = json.dumps({
            'id': self.id if uuid is None else uuid
        })
        r.publish(self.channel, message)

    def _queue_children(self):
        r = self.redis_instance()
        for i in range(len(self.children)):
            child = self.children[i]

            if isinstance(child, str) or isinstance(child, int):
                if r.get(child) is None:
                    raise Exception(f'Invalid task id found in children: {child}. Are you sure it has been queued?')
                
            elif isinstance(child, BaseTask):
                child.queue()
                self.children[i] = child.id
            else:
                raise Exception(f"Got invalid child type: {type(child)}!")
                
    @classmethod
    def unpickle(cls, b: bytes):
        return pickle.loads(b)
    