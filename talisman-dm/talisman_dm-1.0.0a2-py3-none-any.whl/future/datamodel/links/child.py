from dataclasses import dataclass
from typing import Iterable, Iterator

from tdm.future.abstract.datamodel import AbstractNode, AbstractNodeLink, Identifiable
from tdm.future.datamodel.mentions import NodeMention


@dataclass(frozen=True)
class _ChildNodeLink(AbstractNodeLink[NodeMention, NodeMention]):
    order: int

    def __post_init__(self):
        if isinstance(self.source, AbstractNode):
            object.__setattr__(self, 'source', NodeMention(self.source))
        if isinstance(self.target, AbstractNode):
            object.__setattr__(self, 'target', NodeMention(self.target))
        object.__setattr__(self, 'id', self.target.node_id)


@dataclass(frozen=True)
class ChildNodeLink(Identifiable, _ChildNodeLink):
    pass


def create_child_links(source: AbstractNode, targets: Iterable[AbstractNode], *, ordered: bool = True, start: int = 0) \
        -> Iterator[ChildNodeLink]:
    for i, target in enumerate(targets, start=start):
        yield ChildNodeLink(source=NodeMention(source), target=NodeMention(target), order=i if ordered else None)
