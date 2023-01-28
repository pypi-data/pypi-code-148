"""Module for getting full paths."""
from __future__ import annotations

import pathlib
import typing


def path(__path: str, /) -> pathlib.Path:
    """Return the full path of the given path."""
    return pathlib.Path(__path).expanduser().resolve()


def exists(__path: typing.Union[str, pathlib.Path], /) -> bool:
    """Return True if the given path exists."""
    return path(__path).exists()
