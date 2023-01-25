import json
from dataclasses import dataclass
from typing import Self, Any, Dict

from bot_plugin.domain.access_type import AccessType
from bot_plugin.domain.base.serializable import JsonSerializable
from bot_plugin.domain.plugin_context import PluginContext


@dataclass
class PluginRequest(JsonSerializable):
    url: str
    context: PluginContext
    access_type: AccessType = AccessType.PUBLIC

    @classmethod
    def from_json(cls, json_dict: Dict[str, Any]) -> Self:
        return {
            'url' in json_dict: lambda: PluginRequest(**json_dict),
            'resource_id' in json_dict: lambda: PluginContext(**json_dict)
        }.get(True, lambda: json_dict)()

