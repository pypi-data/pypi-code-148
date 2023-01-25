from pathlib import Path
from shlex import quote
from typing import Optional, assert_type

from ..common import ActionType

__all__: list[str] = ["format_message"]


OVERWRITE: str = "(OVERWRITE)"
OVERWRITE_MARKUP: str = (
    "[logging.level.warning]" + OVERWRITE + "[/logging.level.warning]"
)


def to_str(path: str | Path, overwrite: bool = False, markup: bool = False) -> str:
    if overwrite and Path(path).exists():
        return quote(str(path)) + " " + (OVERWRITE_MARKUP if markup else OVERWRITE)
    else:
        return quote(str(path))


def src_to_dst(src: str | Path, dst: str | Path, markup: bool = False) -> str:
    return (
        to_str(path=src, overwrite=False, markup=markup)
        + " -> "
        + to_str(path=dst, overwrite=True, markup=markup)
    )


def format_message(
    message: Optional[str] = None,
    action: Optional[str | ActionType] = None,
    src: Optional[str | Path] = None,
    dst: Optional[str | Path] = None,
    markup: bool = False,
) -> str:
    if message:
        return message

    if src and dst:
        message = src_to_dst(src=src, dst=dst)
    elif src:
        message = to_str(path=src, overwrite=False, markup=markup)
    elif dst:
        message = to_str(path=dst, overwrite=True, markup=markup)
    assert_type(message, Optional[str])

    if action:
        action = str(action).ljust(8)
    assert isinstance(action, Optional[str])

    if action and message:
        return f"{action}: {message}"
    elif action:
        return action
    elif message:
        return message
    else:
        return ""
