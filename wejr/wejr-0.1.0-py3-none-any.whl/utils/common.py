import json
from dataclasses import asdict


class DataclassJsonDictTransformMixin:
    @classmethod
    def from_dict(cls, request_data: dict) -> "DataclassJsonDictTransformMixin":
        return cls(**request_data)

    @classmethod
    def from_json_str(
        cls, request_json: str, **kwargs
    ) -> "DataclassJsonDictTransformMixin":
        return cls(**json.loads(request_json, **kwargs))

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)
