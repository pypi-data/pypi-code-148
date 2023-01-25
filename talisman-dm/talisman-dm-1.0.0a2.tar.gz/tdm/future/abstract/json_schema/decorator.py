from typing import Type, TypeVar

from tdm.future.abstract.datamodel import AbstractDirective, AbstractFact, AbstractNode, AbstractNodeLink, AbstractNodeMention
from .composite import ModelsGenerator

_MODELS_GENERATORS = {
    AbstractDirective: ModelsGenerator(AbstractDirective),
    AbstractFact: ModelsGenerator(AbstractFact),
    AbstractNodeLink: ModelsGenerator(AbstractNodeLink),
    AbstractNodeMention: ModelsGenerator(AbstractNodeMention),
    AbstractNode: ModelsGenerator(AbstractNode, include_label=True)
}

_Element = TypeVar('_Element')


def get_model_generator(cls: Type[_Element]) -> ModelsGenerator[_Element]:
    for cls_, generator in _MODELS_GENERATORS.items():
        if issubclass(cls, cls_):
            return generator
    raise TypeError(f"There is no model generator for {cls}. Available: {tuple(_MODELS_GENERATORS)}")


def generate_model(cls: type = None, *, label: str = None):
    def wrapper(cls_: type):
        return get_model_generator(cls_).generate_model(cls_, label=label)

    if cls is None:
        return wrapper
    return wrapper(cls)
