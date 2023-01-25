import os
from pathlib import Path

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm
from .remove import remove


def link(
    src: str | Path,
    dst: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(action=ActionType.LINK, src=src, dst=dst, markup=True)

    if not confirm(
        default=default,
        confirm_type=confirm_type,
        action=ActionType.COPY,
        src=src,
        dst=dst,
    ):
        logger.skipped(message=message)
        return

    src = Path(src)
    dst = Path(dst)
    if dst.exists():
        remove(path=dst)
    os.symlink(src=src, dst=dst, target_is_directory=src.is_dir())

    logger.success(message=message)
