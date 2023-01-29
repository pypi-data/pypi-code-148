from typing import Sized

from noldor import Validator


def longer_than(lower_bound: int) -> Validator[Sized]:
    return Validator[Sized](
        lambda x: len(x) > lower_bound, f"longer than {lower_bound}"
    )


def shorter_than(upper_bound: int) -> Validator[Sized]:
    return Validator[Sized](
        lambda x: len(x) < upper_bound, f"shorter than {upper_bound}"
    )
