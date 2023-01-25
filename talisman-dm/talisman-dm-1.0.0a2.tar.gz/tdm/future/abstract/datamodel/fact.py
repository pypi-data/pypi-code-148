from dataclasses import dataclass
from enum import Enum
from functools import total_ordering
from typing import Generic, Optional, TypeVar

from .base import EnsureIdentifiable


@total_ordering
class FactStatus(str, Enum):
    def __new__(cls, name: str, priority: int):
        obj = str.__new__(cls, name)
        obj._value_ = name
        obj.priority = priority
        return obj

    APPROVED = ("approved", 0)
    DECLINED = ("declined", 1)
    AUTO = ("auto", 2)
    HIDDEN = ("hidden", 3)
    NEW = ("new", 4)

    def __lt__(self, other: 'FactStatus'):
        if not isinstance(other, FactStatus):
            return NotImplemented
        return self.priority < other.priority


@dataclass(frozen=True)
class AbstractFact(EnsureIdentifiable):
    status: FactStatus


_ST = TypeVar('_ST', bound=AbstractFact)
_TT = TypeVar('_TT', bound=AbstractFact)


@dataclass(frozen=True)
class AbstractLinkFact(AbstractFact, Generic[_ST, _TT]):
    type_id: str
    source: _ST
    target: _TT
    value: Optional[str] = None
