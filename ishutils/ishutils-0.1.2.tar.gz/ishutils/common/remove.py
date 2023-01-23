import os
import shutil
from pathlib import Path

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm

__all__: list[str] = ["remove"]


def remove(
    path: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(action=ActionType.REMOVE, src=path, markup=True)

    if not confirm(
        default=default, confirm_type=confirm_type, action=ActionType.REMOVE, src=path
    ):
        logger.skipped(message=message)

    path = Path(path)
    if path.is_file():
        os.remove(path=path)
    elif path.is_dir():
        shutil.rmtree(path=path)
    else:
        logger.skipped(message=message)
        return

    logger.success(message=message)
