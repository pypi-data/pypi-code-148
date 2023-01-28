import marshal, types
import logging

from typing import Optional, Callable, Union

from .status import TaskStatus
from .lifetime import TaskLifetime
from ...models.base import BaseModel
from ...exceptions.tasks import TaskException


class BaseTask(BaseModel):
    action: Callable
    status: TaskStatus = TaskStatus.NONE
    lifetime: TaskLifetime = TaskLifetime()
    tin: Optional[dict] = None
    tout: Optional[dict] = None

    children: list = []
    parent: Optional[str] = None
    
    @property
    def has_parent(self) -> bool:
        return self.parent is not None
    
    @property
    def has_children(self) -> bool:
        return bool(len(self.children))

    def queue(self, **kwargs):
        self.tin = kwargs
        self.status = TaskStatus.QUEUED

    def digest(self):
        try:
            self.lifetime.start()
            self.status = TaskStatus.RUNNING
            self.tout = self.action(**self.tin)
            self.status = TaskStatus.SUCCEEDED
        except Exception as e:
            self.lifetime.error = e
            self.status = TaskStatus.FAILED
        finally:
            self.lifetime.end()

    def add_child_tid(self, tid: Union[str, int]):
        self.children.append(tid)

    def add_child(self, task):
        self.children.append(task)

    def set_parent(self, tid: Union[str, int]):
        if self.has_parent:
            logging.warning('This task already has a parent, overriding.')
        self.parent = tid
