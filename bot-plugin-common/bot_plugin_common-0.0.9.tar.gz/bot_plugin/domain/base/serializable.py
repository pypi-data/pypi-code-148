import abc
import json
from typing import Dict, Any, Self


class JsonSerializable(abc.ABC):
    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)

    @classmethod
    @abc.abstractmethod
    def from_json(cls, json_dict: Dict[str, Any]) -> Self:
        pass
