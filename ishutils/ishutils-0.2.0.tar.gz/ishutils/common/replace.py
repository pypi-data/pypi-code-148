from pathlib import Path

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm
from .copy import copy
from .remove import remove


def replace(
    src: str | Path,
    dst: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(
        action=ActionType.REPLACE, src=src, dst=dst, markup=True
    )

    if not confirm(
        default=default,
        confirm_type=confirm_type,
        action=ActionType.REPLACE,
        src=src,
        dst=dst,
    ):
        logger.skipped(message=message)

    remove(path=dst, confirm_type=ConfirmType.NEVER, default=True)
    copy(src=src, dst=dst, confirm_type=ConfirmType.NEVER, default=True)
    logger.success(message=message)
