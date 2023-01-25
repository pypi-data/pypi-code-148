from collections import defaultdict
from typing import Callable, Dict, ForwardRef, Iterable, List, Optional, Tuple, Type, Union

from pydantic import Field, create_model
from typing_extensions import Annotated

from tdm.future.abstract.datamodel import AbstractNode
from tdm.future.abstract.json_schema import ElementModel, get_model_generator
from tdm.future.datamodel.links import ChildNodeLink
from tdm.future.helper import unfold_union


def register_node_models() -> Tuple[Type[ElementModel[AbstractNode]], Callable[[AbstractNode], ElementModel[AbstractNode]]]:
    import tdm.future.datamodel.nodes as nodes  # we need this import for serializers registration
    nodes

    # TODO: here plugin for extra document nodes could be added

    models, serialize = get_model_generator(AbstractNode).generate_union_model()

    # add children field to all node models. serialize function doesn't generate value for children field
    NodeModel_ = ForwardRef('NodeModel_')  # noqa N806
    kwargs = {
        'children': (Tuple[NodeModel_, ...], tuple())
    }

    model_mapping = {}
    tree_models = []

    for model in unfold_union(models[AbstractNode]):
        tree_model = create_model(f"Tree{model.__name__}", __base__=model, **kwargs)
        model_mapping[model] = tree_model
        tree_models.append(tree_model)

    # now update forward refs for all tree node models
    NodeModel_ = Annotated[Union[tuple(tree_models)], Field(discriminator='type')]  # noqa N806

    for model in tree_models:
        model.update_forward_refs(NodeModel_=NodeModel_)

    # wrap serialize to generate tree node instead of node

    def serialize_node(node: AbstractNode) -> ElementModel[AbstractNode]:
        serialized = serialize(node)
        return model_mapping[type(serialized)].construct(**serialized.__dict__)

    return NodeModel_, serialize_node


NodeModel, serialize_node = register_node_models()


def construct_tree(id2node_model: Dict[str, NodeModel], links: Iterable[ChildNodeLink]) -> Tuple[NodeModel, ...]:
    roots = set(id2node_model)
    children: Dict[str, List[Tuple[Optional[int], str]]] = defaultdict(list)
    for link in links:
        children[link.source.node_id].append((link.order, link.target.node_id))
    for values in children.values():
        values.sort()

    for source_id, targets in children.items():
        target_ids = tuple(t[1] for t in targets)
        for target_id in target_ids:
            roots.remove(target_id)
        id2node_model[source_id].children = tuple(id2node_model[target_id] for target_id in target_ids)
    return tuple(id2node_model.get(i) for i in roots)
