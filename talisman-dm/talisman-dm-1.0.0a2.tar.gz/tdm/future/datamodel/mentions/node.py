from dataclasses import dataclass

from tdm.future.abstract.datamodel import AbstractNodeMention
from tdm.future.abstract.json_schema import generate_model


@generate_model
@dataclass(frozen=True)
class NodeMention(AbstractNodeMention):
    pass
