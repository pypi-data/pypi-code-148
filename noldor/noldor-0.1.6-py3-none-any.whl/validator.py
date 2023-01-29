from dataclasses import dataclass
from typing import Callable, Generic

from noldor import Response
from noldor._typevar import P
from noldor.config import Config


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=False,  # TODO "slots=True" breaks everything. See: https://github.com/python/cpython/issues/90562
)
class Validator(Generic[P]):

    __slots__ = ("condition", "name")

    condition: Callable[[P], bool]
    name: str

    def __call__(self, p: P) -> Response:
        if self.condition(p) is True:
            return Response(True, f"{Config.RESPECTED}: {p} must be {self.name}")
        else:
            return Response(False, f"{Config.NOT_RESPECTED}: {p} must be {self.name}")


def not_(v: Validator[P]) -> Validator[P]:
    return Validator(lambda p: not v.condition(p), f"not {v.name}")
