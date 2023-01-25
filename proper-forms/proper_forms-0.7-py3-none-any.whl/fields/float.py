from __future__ import annotations

from .text import Text


__all__ = ("Float", )


class Float(Text):

    input_type = "number"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault("type", "Not a valid float number.")

    def prepare(self, object_value: str) -> list[str]:
        return [str(object_value)]

    def type(self, value: str) -> float | None:
        try:
            return float(value)
        except ValueError:
            return None
