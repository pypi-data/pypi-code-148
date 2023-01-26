from typing import Dict, Type

from data_snack_dynamic_entity.validate import validate_entity_templates

from data_snack_dynamic_entity.factory.entity_creation import _create_entity

from data_snack_dynamic_entity.types import EntityTemplates


def load_entities(templates: EntityTemplates) -> Dict[str, Type]:
    """
    Creates new Entity types based on provided config.
    Config should contain a valid template that is created according to the schema (see README).

    :param templates: input config containing templates
    :returns: a dictionary with all created Entity types
    """

    validate_entity_templates(templates)
    return {
        entity_name: _create_entity(entity_name, entity_schema)
        for entity_name, entity_schema in templates.items()
    }
