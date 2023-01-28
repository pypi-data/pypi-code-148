import json
import os

from datetime import datetime
from typing import Any, TypeVar
from uuid import uuid4

from sqlalchemy import String, Column, DATETIME
from sqlalchemy.orm import declarative_base

from ..base import BaseDatabaseModel
from ...managers.sql import SQLModelManager

T = TypeVar('T')


class BaseSQLModel:
    """
        SQL config
    """
    __table_args__ = {'mysql_engine': 'InnoDB'}

    """
        Base columns
    """
    id = Column(String(32), primary_key=True)

    created_at = Column(DATETIME(), default=datetime.utcnow(), nullable=False)
    updated_at = Column(DATETIME(), default=datetime.utcnow(), nullable=False)
    deleted_at = Column(DATETIME(), default=None, nullable=True)

    """
        Methods
    """
    def save(self):
        if self.exists(self.id):
            self.updated_at = datetime.utcnow()
            return self.manager().update(self)
        else:
            self.id = uuid4().hex
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            return self.manager().insert(self)

    def delete(self):
        return self.manager().delete(self)

    def map_to(self, cls):
        return cls.from_dict(self.dict())

    def dict(self):
        return self.__dict__

    """
        Properties
    """
    @property
    def classname(self) -> str:
        return self.__class__.__name__

    """
        Class methods
    """
    @classmethod
    def map_from(cls, item: BaseDatabaseModel):
        return cls.from_dict(item.dict())

    @classmethod
    def from_dict(cls, values: dict) -> Any:
        return cls(**values)

    @classmethod
    def from_json(cls, data: str) -> Any:
        return cls.from_dict(json.loads(data))

    @classmethod
    def get(cls, id: str):
        return cls.manager().get(cls, id)

    @classmethod
    def all(cls, *args, **kwargs):
        return cls.manager().all(cls, **kwargs)

    @classmethod
    def paginate(cls, *args, **kwargs):
        return cls.manager().paginate(cls, *args, **kwargs)

    @classmethod
    def exists(cls, id: str):
        return cls.manager().exists(cls, id)

    @classmethod
    def manager(cls):
        return SQLModelManager[cls](os.environ.get('SQL_CONNECTION_STRING'))


SQLBase = declarative_base(cls=BaseSQLModel)
