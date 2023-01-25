from typing import Type

from tdm.future.abstract.datamodel import AbstractFact
from tdm.future.abstract.json_schema import AbstractLabeledModel, get_model_generator


def register_fact_models() -> Type[AbstractLabeledModel[AbstractFact]]:
    import tdm.future.datamodel.facts as facts  # we need this import for serializers registration
    facts

    # TODO: here plugin for extra document nodes could be added

    return get_model_generator(AbstractFact).generate_labeled_model('FactsModel')


FactsModel = register_fact_models()
