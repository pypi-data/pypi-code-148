from functools import reduce

from noldor import Response, Validator
from noldor._typevar import P


def check(p: P, *validators: Validator[P]) -> Response:
    responses = map(lambda v: v(p), validators)
    return reduce(Response.compose, responses)


def validate(p: P, *validators: Validator[P]) -> None:
    res = check(p, *validators)
    if res.result is False:
        raise ValueError(res.log)
