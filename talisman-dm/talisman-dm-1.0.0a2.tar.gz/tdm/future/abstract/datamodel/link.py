from dataclasses import dataclass
from typing import Generic, TypeVar

from .base import EnsureIdentifiable
from .mention import AbstractNodeMention

_ST = TypeVar('_ST', bound=AbstractNodeMention)
_TT = TypeVar('_TT', bound=AbstractNodeMention)


@dataclass(frozen=True)
class AbstractNodeLink(EnsureIdentifiable, Generic[_ST, _TT]):
    source: _ST
    target: _TT
