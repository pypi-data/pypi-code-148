from math import floor, sqrt

from noldor import Validator


def multiple_of(p: int) -> Validator[int]:
    return Validator[int](
        lambda n: (p != 0 and n % p == 0) or (p == 0 and n == 0),
        f"multiple of {p}",
    )


def is_prime() -> Validator[int]:
    return Validator[int](
        lambda x: x > 1
        and not any(multiple_of(i)(x).result for i in range(2, floor(sqrt(x)) + 1)),
        "prime",
    )
