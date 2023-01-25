from dataclasses import dataclass

from tdm.future.abstract.datamodel import AbstractNodeMention
from tdm.future.abstract.json_schema import generate_model
from tdm.future.datamodel.nodes import ImageNode


@generate_model
@dataclass(frozen=True)
class ImageNodeMention(AbstractNodeMention):
    node: ImageNode
    top: int
    bottom: int
    left: int
    right: int

    def __post_init__(self):
        if not isinstance(self.node, ImageNode):
            raise ValueError(f"Incorrect node type {type(self.node)}. Expected {ImageNode}")
        if self.top < 0 or self.bottom <= self.top or self.left < 0 or self.right <= self.left:
            raise ValueError(f"Incorrect bbox [({self.top}, {self.left}); ({self.bottom}, {self.right})]")
