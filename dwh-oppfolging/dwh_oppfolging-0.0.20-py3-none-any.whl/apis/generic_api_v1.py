"read json from endpoint"


from typing import Any
import requests
from dwh_oppfolging.transforms.datatypes import FlatSchema
from dwh_oppfolging.transforms.functions import flatten_dict, get_fields_in_dict


def get_json_from_url(
    url: str,
    schema: FlatSchema | None = None,
    separator = "_",
    flatten_lists: bool = False
) -> dict[str, Any]:
    """
    returns json encoded content from url or optionally converted with flattened schema
    """
    json_object = requests.get(url, timeout=20).json()
    if schema is not None:
        return get_fields_in_dict(flatten_dict(json_object, separator, flatten_lists), schema)
    return json_object
