from __future__ import annotations

import typing as t


__all__ = ("type_boolean",)


default_false_values = ("", "none", "0", "no", "nope", "nah", "off", "false")


def type_boolean(
    value: str, false_values: t.Sequence[str] = default_false_values
) -> bool:
    if value in (False, None):
        return False
    if str(value).strip().lower() in false_values:
        return False
    return True
