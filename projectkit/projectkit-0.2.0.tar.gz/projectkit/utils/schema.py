import inspect
from collections import defaultdict
from functools import reduce
from typing import Iterable

from projectkit.model.project import ProjectKitClassCLS, BaseProjectKitModel, BaseProjectKitClass


def extended_schema(
    project_kit_class: ProjectKitClassCLS, with_optional: bool = True, with_required: bool = True
) -> dict:
    assert with_optional or with_required

    if issubclass(project_kit_class, BaseProjectKitModel):
        class_schema = project_kit_class.schema()
        required = (
            field_name_to_metadata(class_schema["required"], class_schema, project_kit_class)
            if "required" in class_schema
            else {}
        )
        optional = field_name_to_metadata(
            set(class_schema["properties"]).difference(required), class_schema, project_kit_class
        )
    elif issubclass(project_kit_class, BaseProjectKitClass):
        class_init_parameters = inspect.signature(project_kit_class.__init__).parameters
        required, optional = {}, {}
        for name, parameter in class_init_parameters.items():
            if name == "self":
                continue
            if parameter.default == inspect._empty:
                required[name] = parameter.annotation
            else:
                optional[name] = (f"default: {parameter.default}", parameter.annotation)
    else:
        raise ValueError(f"Unsupported class, {project_kit_class.__name__}")

    defined, result = [], {}
    if required and with_required:
        defined.extend(required)
        result["required"] = required
    if with_optional:
        result["optional"] = optional

    return {"defined": {field: "" for field in defined}, **result}


def extended_group_schema(project_kit_classes: Iterable, *args, **kwargs) -> dict:
    schemas = {
        project_kit_class.__name__: extended_schema(project_kit_class, *args, **kwargs)
        for project_kit_class in project_kit_classes
    }
    schema_names = tuple(schemas)
    first = schemas[schema_names[0]]

    specific, common = defaultdict(dict), {}
    for component in first:
        # Reduce till we have keys present in every set
        common_keys = set(reduce(set.intersection, map(lambda x: set(x[component]), schemas.values())))
        # Common keys are present in every schema; we can just get the metadata, v, from the first
        common[component] = {k: v for k, v in first[component].items() if k in common_keys}

        for name, schema in schemas.items():
            if difference := set(schema[component]).difference(common_keys):
                specific[name][component] = {k: v for k, v in schema[component].items() if k in difference}
            else:
                specific[name] = {"defined": {}}

    return {"common": common, "specific": dict(specific)}


def field_name_to_metadata(fields: Iterable, class_schema: dict, project_kit_class: ProjectKitClassCLS) -> dict:
    result = {}
    for name in sorted(fields):
        if name in project_kit_class.project_kit_fields_to_exclude_from_settings_schema:
            continue

        field_property = class_schema["properties"][name]
        if "type" in field_property:
            field_type = field_property["type"]
        elif "anyOf" in field_property:
            field_type = field_property["anyOf"]
        elif "allOf" in field_property:
            field_type = field_property["allOf"]
        else:
            field_type = None

        if "default" in field_property:
            result[name] = f"{field_type} -> {field_property['default']}"
        else:
            result[name] = str(field_type)

    return result
