from dataclasses import dataclass

from tdm.future.abstract.datamodel import AbstractNodeLink, AbstractNodeMention, Identifiable
from tdm.future.abstract.json_schema import generate_model


@generate_model(label='same')
@dataclass(frozen=True)
class SameNodeLink(Identifiable, AbstractNodeLink[AbstractNodeMention, AbstractNodeMention]):
    pass


@generate_model(label='translation')
@dataclass(frozen=True)
class TranslationNodeLink(Identifiable, AbstractNodeLink[AbstractNodeMention, AbstractNodeMention]):
    pass


@generate_model(label='reference')
@dataclass(frozen=True)
class ReferenceNodeLink(Identifiable, AbstractNodeLink[AbstractNodeMention, AbstractNodeMention]):
    pass
