from typing import TypeVar, Callable
from reactivex import Observable, operators

_T = TypeVar('_T')

def item_at_index(index: int) -> Callable[[Observable[list[_T]]], Observable[_T]]:
    return operators.map(
        lambda x: x[index]
    )