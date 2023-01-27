from enum import Enum
from math import sin
from typing import List, Optional, Tuple, Union

import rustga


class SearchRange:
    pass


class SteppedRange(SearchRange):
    def __init__(self, param_range: Union[Tuple[float, float], Tuple[float, float, Optional[float]]]) -> None:
        super(SteppedRange, self).__init__()
        self._lower = param_range[0]
        self._upper = param_range[1]
        self._step = param_range[2] if len(param_range) >= 3 else None  # type:ignore

def score_fn(X: list) -> list[float]:
    """Score func.

    Args:
        X (list): batch * dim.

    Returns:
        float: scores
    """
    return [sin(sum(x)) ** 2 for x in X]

param = rustga.GAParams(2, 100, 300, 100, 0.1, 0.1, 0.1, 3)
explanatories = {
        "x1": SteppedRange((0, 10.0, 0.1)),
        "x2": SteppedRange((0, 10.0, 0.1)),
    }
ga = rustga.GASolver(score_fn, param)
for rng in explanatories.values():
    if isinstance(rng, SteppedRange) and rng._step is not None:
        ga.add_stepped_range((rng._lower, rng._upper, rng._step))

print("ans: ", ga.run())
