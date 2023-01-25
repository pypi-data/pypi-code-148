import dataclasses
from dataclasses import fields
from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel, Extra, create_model
from typing_extensions import Literal, Self

from tdm.future.helper import cache_result, generics_mapping, is_subclass
from .serializers import AbstractElementModel, AbstractElementSerializer, BaseSerializers

_Element = TypeVar('_Element')


class ElementModel(BaseModel, AbstractElementModel[_Element], Generic[_Element]):
    class Config:
        extra = Extra.forbid

    def deserialize(self, typed_id2element: Dict[type, Dict[str, Any]]) -> _Element:
        raise NotImplementedError

    @classmethod
    def serialize(cls, element: _Element) -> Self:
        kwargs = {}
        for key, value in element.__dict__.items():
            for type_, serializer in BaseSerializers.items():
                if isinstance(value, type_):
                    kwargs[key] = serializer.serialize(value)
                    break
            else:
                kwargs[key] = value
        return cls.construct(**kwargs)


_BaseType = TypeVar('_BaseType', bound=type)


@cache_result()
def create_model_for_type(type_: Type[_Element], label: Optional[str] = None) -> Type[ElementModel[_Element]]:
    type_vars = generics_mapping(type_)

    model_fields = {}

    special_fields: Dict[str, AbstractElementSerializer] = {}

    for field in fields(type_):
        name = field.name
        default_value = field.default if field.default is not dataclasses.MISSING else ...
        field_type = type_vars.get(field.type, field.type)
        for _type, serializer in BaseSerializers.items():
            if is_subclass(field_type, _type):
                field_type = serializer.field_type(field_type)
                special_fields[name] = serializer
        model_fields[name] = (field_type, default_value)
    if label:
        model_fields['type'] = (Literal[label], label)

    model = create_model(f"{type_.__name__}Model", __base__=ElementModel, **model_fields)

    def deserialize(self: model, typed_id2element: Dict[type, Dict[str, Any]]) -> type_:
        kwargs = {}
        for f in set(type_.__dataclass_fields__).intersection(self.__dict__):
            kwargs[f] = getattr(self, f)
            if f in special_fields:
                kwargs[f] = special_fields[f].deserialize(kwargs[f], typed_id2element)
        return type_(**kwargs)

    model.deserialize = deserialize

    return model
