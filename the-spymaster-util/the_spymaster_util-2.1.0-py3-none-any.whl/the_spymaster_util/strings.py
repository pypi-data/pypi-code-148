import re
from typing import Type, TypeVar, Union

CAMEL_TO_CONST_1 = re.compile(r"(.)([A-Z][a-z]+)")
CAMEL_TO_CONST_2 = re.compile(r"([a-z0-9])([A-Z])")
T = TypeVar("T")


def camel_to_const(string: str) -> str:
    string = CAMEL_TO_CONST_1.sub(r"\1_\2", string)
    return CAMEL_TO_CONST_2.sub(r"\1_\2", string).upper()


def get_class_name(instance_or_class: Union[T, Type[T]]):
    clazz = instance_or_class if isinstance(instance_or_class, type) else instance_or_class.__class__
    return clazz.__name__
