import enum
from dataclasses import dataclass
from typing import Union, Dict, Any, Self

from bot_plugin.domain.base.serializable import JsonSerializable
from bot_plugin.domain.plugin_context import PluginContext


class CallbackQueryMethod(str, enum.Enum):
    CREATE = 'CREATE'
    SELECT = 'SELECT_ONE'
    SELECT_MULTIPLE = 'SELECT_MULTIPLE'
    EDIT = 'EDIT'
    DELETE = 'DELETE'


class MessageMethod(str, enum.Enum):
    INPUT = 'INPUT'
    REPLY = 'REPLY'
    INLINE = 'INLINE'


@dataclass
class CallbackQueryEventRequest:
    user_id: Union[str, int]


@dataclass
class MessageEventRequest(JsonSerializable):
    user_id: Union[str, int]
    text: str

    @classmethod
    def from_json(cls, json_dict: Dict[str, Any]) -> Self:
        return {
            'user_id' in json_dict: lambda: MessageEventRequest(**json_dict),
        }.get(True, lambda: json_dict)()


@dataclass
class MessageEventResponse(JsonSerializable):
    method: MessageMethod
    context: PluginContext

    @classmethod
    def from_json(cls, json_dict: Dict[str, Any]) -> Self:
        return {
            'method' in json_dict: lambda: MessageEventResponse(**json_dict),
        }.get(True, lambda: json_dict)()
