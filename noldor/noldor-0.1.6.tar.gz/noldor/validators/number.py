"""
TODO This module can be generalized to any class supporting comparison.
However, I haven't found a way to point out such a class in Python.
[A comparable type?](https://github.com/python/typing/issues/59)
"""
from typing import TypeVar

from noldor import Validator

Number = TypeVar("Number", int, float)


def greater_than(lower_bound: Number) -> Validator[Number]:
    return Validator[Number](lambda x: x > lower_bound, f"greater than {lower_bound}")


def lower_than(upper_bound: Number) -> Validator[Number]:
    return Validator[Number](lambda x: x < upper_bound, f"lower than" f" {upper_bound}")


def is_positive() -> Validator[Number]:
    return Validator[Number](lambda x: x > 0, "positive")
