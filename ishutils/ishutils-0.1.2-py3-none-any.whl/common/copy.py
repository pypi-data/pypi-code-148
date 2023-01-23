import os
import shutil
from pathlib import Path

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm

__all__: list[str] = ["copy"]


def copy(
    src: str | Path,
    dst: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(action=ActionType.COPY, src=src, dst=dst, markup=True)

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
    os.makedirs(dst.parent, exist_ok=True)
    if src.is_file():
        shutil.copy2(src=src, dst=dst)
    elif src.is_dir():
        shutil.copytree(src=src, dst=dst)
    else:
        raise FileNotFoundError(src)

    logger.success(message=message)
