from uuid import uuid4
from typing import Optional
from datetime import datetime

from ...models.base import BaseModel


class TaskLifetime(BaseModel):
    id: str = uuid4().hex
    created: datetime = datetime.utcnow()
    started: Optional[datetime] = None
    ended: Optional[datetime] = None
    error: Optional[Exception] = None
    
    @property
    def took(self) -> datetime:
        return self.ended - self.started

    def start(self):
        self.started = datetime.utcnow()

    def end(self):
        self.ended = datetime.utcnow()
