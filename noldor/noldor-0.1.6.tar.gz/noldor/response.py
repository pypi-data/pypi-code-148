from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    init=True,
    repr=False,
    eq=False,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=True,
)
class Response:

    result: bool
    log: str

    def compose(self: Response, other: Response) -> Response:
        result = self.result and other.result
        log = f"{self.log}\n{other.log}"
        return Response(result, log)
