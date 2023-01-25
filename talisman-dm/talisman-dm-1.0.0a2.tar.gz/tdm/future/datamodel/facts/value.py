from dataclasses import dataclass
from typing import Sequence, Tuple, Union

from frozendict import frozendict

from tdm.future.abstract.datamodel import AbstractFact, Identifiable
from tdm.future.abstract.json_schema import generate_model


@dataclass(frozen=True)
class _AtomValueFact(AbstractFact):
    type_id: str
    value: Union[dict, Tuple[dict, ...]] = tuple()

    def __post_init__(self):
        if isinstance(self.value, dict):
            object.__setattr__(self, 'value', frozendict(self.value))
        elif isinstance(self.value, Sequence):
            object.__setattr__(self, 'value', tuple(frozendict(v) for v in self.value))


@generate_model(label='atom')
@dataclass(frozen=True)
class AtomValueFact(Identifiable, _AtomValueFact):
    pass


@dataclass(frozen=True)
class _CompositeValueFact(AbstractFact):
    type_id: str


@generate_model(label='composite')
@dataclass(frozen=True)
class CompositeValueFact(Identifiable, _CompositeValueFact):
    pass
