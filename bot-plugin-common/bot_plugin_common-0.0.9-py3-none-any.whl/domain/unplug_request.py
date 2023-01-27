from dataclasses import dataclass
from typing import Dict, Any, Self

from bot_plugin.domain.base.serializable import JsonSerializable


@dataclass
class UnplugRequest(JsonSerializable):
    url: str

    @classmethod
    def from_json(cls, json_dict: Dict[str, Any]) -> Self:
        return {
            'url' in json_dict: lambda: UnplugRequest(**json_dict),
        }.get(True, lambda: json_dict)()
