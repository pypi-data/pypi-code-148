from tdm.future.abstract.datamodel import AbstractFact, AbstractNode, AbstractNodeMention, BaseNodeMetadata
from .identifiable import IdSerializer
from .mention import NodeMentionSerializer
from .metadata import NodeMetadataSerializer


def build_serializers():
    result = {
        AbstractNode: IdSerializer(AbstractNode),
        AbstractFact: IdSerializer(AbstractFact),
        AbstractNodeMention: NodeMentionSerializer(),
        BaseNodeMetadata: NodeMetadataSerializer()
    }
    # other serializers could be added here
    return result
