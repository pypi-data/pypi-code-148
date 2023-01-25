from dataclasses import dataclass
from typing import Union

from tdm.future.abstract.datamodel import AbstractLinkFact, Identifiable
from tdm.future.abstract.json_schema import generate_model
from .concept import ConceptFact
from .value import AtomValueFact, CompositeValueFact


@generate_model(label='relation')
@dataclass(frozen=True)
class RelationFact(Identifiable, AbstractLinkFact[ConceptFact, ConceptFact]):
    pass


ValueFact = Union[AtomValueFact, CompositeValueFact]


@generate_model(label='property')
@dataclass(frozen=True)
class PropertyFact(Identifiable, AbstractLinkFact[ConceptFact, ValueFact]):
    pass


@generate_model(label='r_property')
@dataclass(frozen=True)
class RelationPropertyFact(Identifiable, AbstractLinkFact[RelationFact, ValueFact]):
    pass


@generate_model(label='slot')
@dataclass(frozen=True)
class SlotFact(Identifiable, AbstractLinkFact[CompositeValueFact, ValueFact]):
    pass
