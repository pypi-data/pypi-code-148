from typing import Optional
from datetime import datetime
from uuid import uuid4

from . import BaseModel


class BaseDatabaseModel(BaseModel):
    id: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id is None:
            self.id = kwargs.get('id', uuid4().hex)

    def save(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            self.updated_at = datetime.utcnow()

    def delete(self):
        self.deleted_at = datetime.utcnow()