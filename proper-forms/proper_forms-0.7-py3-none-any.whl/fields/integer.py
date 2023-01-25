from __future__ import annotations

from .text import Text


__all__ = ("Integer", )


class Integer(Text):

    input_type = "number"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault("type", "Not a valid integer.")

    def prepare(self, object_value: int) -> list[str]:
        return [str(object_value)]

    def type(self, value: str) -> int | None:
        try:
            return int(value)
        except ValueError:
            return None
