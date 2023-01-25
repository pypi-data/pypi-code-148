import shutil
from pathlib import Path

from ..logging import ActionType, Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm

__all__: list[str] = ["move"]


def move(
    src: str | Path,
    dst: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(action=ActionType.MOVE, src=src, dst=dst, markup=True)

    if not confirm(
        default=default,
        confirm_type=confirm_type,
        action=ActionType.MOVE,
        src=src,
        dst=dst,
    ):
        logger.skipped(message=message)
        return

    shutil.move(src=src, dst=dst)

    logger.success(message=message)
