from dataclasses import asdict
from typing import Any, Generic, List, TypeVar


T = TypeVar("T")


class DataclassBuilder(Generic[T]):
    def __init__(self, dataclass: T) -> None:
        self.dataclass = dataclass

    async def build_dict(self, remove_types: List[Any]):
        data = asdict(self.dataclass)
        return {
            key: data[key]
            for key in data.keys()
            if bool([isinstance(data[key], _type) for _type in remove_types])
        }
