import json

from typing import Any
from pydantic import BaseModel as BasePydanticModel


class BaseModel(BasePydanticModel):
    # Pydantic config
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    '''
        Properties
    '''

    @property
    def properties(self) -> set:
        return set([str(col) for col in self.dict().keys()])

    @property
    def values(self) -> set:
        return set(self.dict().values())

    @property
    def classname(self) -> str:
        return self.__class__.__name__

    '''
        Class methods
    '''

    @classmethod
    def from_dict(cls, values: dict) -> Any:
        return cls(**values)

    @classmethod
    def from_json(cls, data: str) -> Any:
        return cls.from_dict(json.loads(data))
