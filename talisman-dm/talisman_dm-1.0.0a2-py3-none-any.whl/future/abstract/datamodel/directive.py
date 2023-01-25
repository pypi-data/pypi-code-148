from dataclasses import dataclass

from .base import EnsureIdentifiable


@dataclass(frozen=True)
class AbstractDirective(EnsureIdentifiable):
    pass
