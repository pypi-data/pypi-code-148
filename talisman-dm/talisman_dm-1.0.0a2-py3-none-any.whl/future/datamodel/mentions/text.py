from dataclasses import dataclass

from tdm.future.abstract.datamodel import AbstractNodeMention
from tdm.future.abstract.json_schema import generate_model
from tdm.future.datamodel.nodes import TextNode


@generate_model
@dataclass(frozen=True)
class TextNodeMention(AbstractNodeMention):
    node: TextNode
    start: int
    end: int

    def __post_init__(self):
        if not isinstance(self.node, TextNode):
            raise ValueError(f"Incorrect node type {type(self.node)}. Expected {TextNode}")
        if self.start < 0 or self.end <= self.start:
            raise ValueError(f"Incorrect span [{self.start}, {self.end})")
