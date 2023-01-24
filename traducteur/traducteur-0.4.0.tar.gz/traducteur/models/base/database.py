from typing import Optional
from datetime import datetime
from uuid import uuid4

from . import BaseModel


class BaseDatabaseModel(BaseModel):
    id: str = uuid4().hex

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def save(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
        else:
            self.updated_at = datetime.utcnow()

    def delete(self):
        self.deleted_at = datetime.utcnow()