from enum import Enum
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


class FiniteSet(SearchRange):
    class Kind(Enum):
        Number = 0
        Category = 1
        Molecule = 2

    def __init__(self, params: List[Union[str, float]], kind: Optional[Kind] = None) -> None:
        super(FiniteSet, self).__init__()
        self._params = params
        self._kind = kind


if __name__ == "__main__":
    """ Problem definition
    Maximize: (x1 - 5.0)^2 + x2^2
    Subject to: x1 <= 5.0
    Answer: (0.0, 10.0)
    """
    # x <= 5.0
    def constraint_fn(x: list) -> float:
        return -x[0] + 5.0

    def score_fn(X: list) -> list[float]:
        ret = []
        for x in X:
            validation = constraint_fn(x)
            if validation < 0.0:
                ret.append(validation)
            else:
                ret.append((x[0] - 5.0)**2 + x[1]**2)
        return ret

    param = rustga.GAParams(4, 100, 300, 100, 0.1, 0.1, 0.1, 3)
    explanatories = {
        "x1": SteppedRange((0, 10.0, 0.1)),
        "x2": SteppedRange((0, 10.0, 0.1)),
        # "x3": FiniteSet(["A", "B", "C"]),
    }
    ga = rustga.GASolver(score_fn, param)
    for rng in explanatories.values():
        if isinstance(rng, SteppedRange) and rng._step is not None:
            ga.add_stepped_range((rng._lower, rng._upper, rng._step))
        elif isinstance(rng, FiniteSet) and rng._kind == FiniteSet.Kind.Category:
            ga.add_string_finite_set(rng._params)
    print(ga.genome_builder.length())
    print("ans: ", ga.run())
