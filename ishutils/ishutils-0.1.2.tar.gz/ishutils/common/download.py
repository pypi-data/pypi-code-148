import os
from pathlib import Path

from httpie.core import main

from ..logging import Logger, get_logger
from ..utils.text import format_message
from . import ActionType
from .confirm import ConfirmType, confirm

__all__: list[str] = ["download"]


def download(
    url: str,
    output: str | Path,
    confirm_type: ConfirmType = ConfirmType.DEFAULT,
    default: bool = True,
) -> None:
    logger: Logger = get_logger()
    message: str = format_message(
        action=ActionType.DOWNLOAD, src=url, dst=output, markup=True
    )

    if not confirm(
        default=default,
        confirm_type=confirm_type,
        action=ActionType.DOWNLOAD,
        src=url,
        dst=output,
    ):
        logger.skipped(message=message)
        return

    output = Path(output)
    os.makedirs(name=output.parent, exist_ok=True)
    main(args=["https", "--body", "--output", str(output), "--download", url])

    logger.success(message=message)
