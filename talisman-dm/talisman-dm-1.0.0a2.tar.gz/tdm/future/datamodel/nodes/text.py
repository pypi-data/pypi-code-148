from dataclasses import dataclass
from typing import Optional

from tdm.future.abstract.datamodel import AbstractContentNode, BaseNodeMetadata
from tdm.future.abstract.json_schema import generate_model


@dataclass(frozen=True)
class TextNodeMetadata(BaseNodeMetadata):
    language: Optional[str] = None


@generate_model(label='text')
@dataclass(frozen=True)
class TextNode(AbstractContentNode[TextNodeMetadata, str]):
    pass


@generate_model(label='key')
@dataclass(frozen=True)
class KeyNode(AbstractContentNode[TextNodeMetadata, str]):
    pass
