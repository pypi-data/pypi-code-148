from typing import Type

from tdm.future.abstract.datamodel import AbstractDirective
from tdm.future.abstract.json_schema import AbstractLabeledModel, get_model_generator


def register_directives_model() -> Type[AbstractLabeledModel[AbstractDirective]]:
    import tdm.future.datamodel.directives as directives
    directives

    # TODO: here plugin for extra document nodes could be added

    return get_model_generator(AbstractDirective).generate_labeled_model('DirectivesModel')


DirectivesModel = register_directives_model()
