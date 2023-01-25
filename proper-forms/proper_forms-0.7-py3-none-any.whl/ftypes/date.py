from __future__ import annotations

import datetime
import typing as t


__all__ = ("type_date", )


def type_date(value: t.Any) -> datetime.date | None:
    if value is None:
        return None
    try:
        ldt = [int(f) for f in value.split("-")]
        return datetime.date(*ldt)
    except (ValueError, TypeError):
        return None
