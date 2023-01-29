from typing import Any, Callable

from noldor import Validator
from noldor import validate as val
from noldor._typevar import P


def validate(*validators: Validator[P]) -> Callable[[Any, Any, P], None]:
    return lambda _, __, value: val(value, *validators)
