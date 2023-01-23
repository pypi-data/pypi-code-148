from enum import StrEnum
from pathlib import Path
from typing import Optional, assert_never, assert_type

import questionary

from ..config import config
from ..utils.text import format_message
from . import ActionType

__all__: list[str] = ["ConfirmType", "confirm"]


class ConfirmType(StrEnum):
    ALWAYS = "ALWAYS"
    DEFAULT = "DEFAULT"
    NEVER = "NEVER"
    OVERWRITE = "OVERWRITE"


def confirm(
    message: Optional[str] = None,
    default: bool = True,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    action: Optional[ActionType] = None,
    src: Optional[str | Path] = None,
    dst: Optional[str | Path] = None,
) -> bool:
    if config.yes:
        return True
    message = format_message(message=message, action=action, src=src, dst=dst)
    assert_type(message, str)
    match confirm_type:
        case ConfirmType.ALWAYS:
            response: bool = questionary.confirm(
                message=message, default=default
            ).unsafe_ask()
            return response
        case ConfirmType.DEFAULT:
            return confirm(
                message=message,
                default=default,
                confirm_type=ConfirmType(config.default_confirm_type),
                action=action,
                src=src,
                dst=dst,
            )
        case ConfirmType.NEVER:
            return default
        case ConfirmType.OVERWRITE:
            if dst and Path(dst).exists():
                response: bool = questionary.confirm(
                    message=message, default=default
                ).unsafe_ask()
                return response
            else:
                return default
        case _ as unreachable:
            assert_never(unreachable)
