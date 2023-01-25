from __future__ import annotations

from datetime import date, datetime

from .text import Text
from ..ftypes import type_date


__all__ = ("Date", )


class Date(Text):
    """A simple date field formatted as `YYYY-MM-dd`. Example: "1980-07-28".
    """

    input_type = "date"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.setdefault(
            "type", "Date must have a YYYY-MM-dd format."
        )

    def prepare(self, object_value: date | datetime) -> list[str]:
        return [object_value.strftime("%Y-%m-%d")]

    def type(self, value: str) -> date | None:
        return type_date(value)
