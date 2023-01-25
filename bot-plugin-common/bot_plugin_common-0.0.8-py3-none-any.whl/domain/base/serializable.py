import abc
import json


class JsonSerializable(abc.ABC):
    def to_json(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)
