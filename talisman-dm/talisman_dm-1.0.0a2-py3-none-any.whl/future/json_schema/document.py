from typing import Dict, Iterable, Optional, Set, Tuple

from pydantic import BaseModel
from typing_extensions import Literal

from tdm.future.abstract.datamodel import AbstractNode, AbstractNodeLink
from tdm.future.datamodel.document import TalismanDocument
from tdm.future.datamodel.links import ChildNodeLink
from tdm.future.datamodel.mentions import NodeMention
from tdm.json_schema import DocumentMetadataModel
from .directives import DirectivesModel
from .facts import FactsModel
from .links import NodeLinksModel
from .nodes import NodeModel, construct_tree, serialize_node


class TalismanDocumentModel(BaseModel):
    VERSION: Literal['1.0'] = '1.0'
    id: str
    main_node: str
    content: Tuple[NodeModel, ...]
    links: NodeLinksModel
    facts: FactsModel
    directives: DirectivesModel

    metadata: Optional[DocumentMetadataModel]  # should be removed in future

    def deserialize(self) -> TalismanDocument:
        links: Set[AbstractNodeLink]
        id2node, links = self._collect_nodes()
        links.update(self.links.deserialize(id2node))

        return TalismanDocument(
            content=id2node.values(),
            root=id2node[self.main_node],
            links=links,
            facts=self.facts.deserialize(id2node),
            directives=self.directives.deserialize(id2node),
            metadata=self.metadata.to_metadata() if self.metadata is not None else None,
            id_=self.id
        )

    def _collect_nodes(self) -> Tuple[Dict[str, AbstractNode], Set[ChildNodeLink]]:
        # try to avoid recursion
        children = {}
        id2node = {}

        to_be_processed = list(self.content)

        for node_model in to_be_processed:
            id2node[node_model.id] = node_model.deserialize({})
            children[node_model.id] = [child.id for child in node_model.children]
            to_be_processed.extend(node_model.children)
        links = set()
        for parent_id, child_ids in children.items():
            links.update(
                ChildNodeLink(source=NodeMention(id2node[parent_id]), target=NodeMention(id2node[child_id]), order=i)
                for i, child_id in enumerate(child_ids)
            )

        return id2node, links

    @classmethod
    def serialize(cls, document: TalismanDocument) -> 'TalismanDocumentModel':
        id2node_models = {id_: serialize_node(node) for id_, node in document.content.items()}
        links = dict(document.links)
        children_links: Iterable[ChildNodeLink] = links.pop(ChildNodeLink)
        return cls.construct(
            id=document.id,
            main_node=document.root.id,
            content=construct_tree(id2node_models, children_links),
            links=NodeLinksModel.serialize(links),
            facts=FactsModel.serialize(document.facts),
            directives=DirectivesModel.serialize(document.directives),
            metadata=DocumentMetadataModel(**document._metadata) if document._metadata is not None else None
        )
