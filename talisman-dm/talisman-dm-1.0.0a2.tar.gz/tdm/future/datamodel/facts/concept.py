from dataclasses import dataclass
from typing import Sequence, Tuple, Union

from tdm.future.abstract.datamodel import AbstractFact, Identifiable
from tdm.future.abstract.json_schema import generate_model


@dataclass(frozen=True)
class _ConceptFact(AbstractFact):  # not an error as id argument is kw only
    type_id: str
    value: Union[str, Tuple[str, ...]] = tuple()

    def __post_init__(self):
        if isinstance(self.value, str) or isinstance(self.value, tuple):
            return
        if isinstance(self.value, Sequence):
            object.__setattr__(self, 'value', tuple(self.value))
        else:
            raise ValueError


@generate_model(label='concept')
@dataclass(frozen=True)
class ConceptFact(Identifiable, _ConceptFact):
    pass
