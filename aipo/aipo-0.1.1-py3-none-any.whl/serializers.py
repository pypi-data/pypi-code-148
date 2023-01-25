import base64
import json
from datetime import date, datetime, time
from typing import Any, Dict


class SerializerBase:
    """Base class for serializers.

    For extending this class, you need to implement the following methods:
    """

    def encode(self, obj: Dict[str, Any]) -> str:
        raise NotImplementedError

    def decode(self, obj: str) -> Dict[str, Any]:
        raise NotImplementedError


class JSONSerializer(SerializerBase):
    """JSON serializer."""

    def to_json_type(self, obj: Any) -> Any:
        if type(obj) in (int, float, str, bool, type(None)):
            return obj
        elif type(obj) is dict:
            return {
                "value": {key: self.to_json_type(value) for key, value in obj.items()},
                "type": "dict",
            }
        elif type(obj) is datetime:
            return {"value": obj.isoformat(), "type": "datetime"}
        elif type(obj) is date:
            return {"value": obj.isoformat(), "type": "date"}
        elif type(obj) is time:
            return {"value": obj.isoformat(), "type": "time"}
        elif type(obj) is list:
            return [self.to_json_type(item) for item in obj]
        elif type(obj) is bytes:
            return {
                "value": base64.b64encode(obj).decode("utf8"),
                "type": "bytes",
                "encoding": "base64",
            }

        raise NotImplementedError(f"Unsuported type {type}")

    def parse_type(self, obj: Any) -> Any:
        if type(obj) == (int, float, str, bool, type(None)):
            return obj
        elif type(obj) is list:
            return [self.parse_type(item) for item in obj]
        elif type(obj) is dict:
            obj_type = obj.get("type")
            if obj_type == "dict":
                return {
                    key: self.parse_type(value) for key, value in obj["value"].items()
                }
            elif obj_type == "datetime":
                return datetime.fromisoformat(obj["value"])
            elif obj_type == "date":
                return datetime.fromisoformat(obj["value"]).date()
            elif obj_type == "time":
                return time.fromisoformat(obj["value"])
            elif obj_type == "bytes":
                return base64.b64decode(obj["value"].encode("utf8"))

        raise NotImplementedError(f"Unsuported type {obj_type}")

    def encode(self, obj: Dict[str, Any]) -> str:
        return json.dumps({key: self.to_json_type(value) for key, value in obj.items()})

    def decode(self, obj: str) -> Dict[str, Any]:
        return {key: self.parse_type(value) for key, value in json.loads(obj).items()}
