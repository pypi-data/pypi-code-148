import logging
from typing import Optional, cast

from rich.console import Console
from rich.logging import RichHandler
from rich.style import Style
from rich.theme import Theme

from .common import ActionType, Status

__all__: list[str] = ["Logger", "install", "get_logger"]


NAME: str = "ishutils"


FAILURE: int = logging.ERROR + 1
RUNNING: int = logging.INFO + 1
SKIPPED: int = logging.INFO + 2
SUCCESS: int = logging.INFO + 3


class Logger(logging.Logger):
    def format_message(self, status: str | Status, message: str) -> str:
        status = str(status)
        style: str = f"logging.level.{status.lower()}"
        return f"[{style}]" + message

    def failure(self, message: str) -> None:
        self.log(
            level=FAILURE,
            msg=self.format_message(status=Status.FAILURE, message=message),
            stacklevel=2,
        )

    def running(self, message: str) -> None:
        self.log(
            level=RUNNING,
            msg=self.format_message(status=Status.RUNNING, message=message),
            stacklevel=2,
        )

    def skipped(self, message: str) -> None:
        self.log(
            level=SKIPPED,
            msg=self.format_message(status=Status.SKIPPED, message=message),
            stacklevel=2,
        )

    def success(self, message: str) -> None:
        self.log(
            level=SUCCESS,
            msg=self.format_message(status=Status.SUCCESS, message=message),
            stacklevel=2,
        )


def install(
    format: str = "%(message)s",
    level: int | str = logging.INFO,
    console: Optional[Console] = None,
    keywords: Optional[list[str]] = [e.value + " " for e in ActionType],
) -> None:
    logging.addLevelName(level=FAILURE, levelName="FAILURE")
    logging.addLevelName(level=RUNNING, levelName="RUNNING")
    logging.addLevelName(level=SKIPPED, levelName="SKIPPED")
    logging.addLevelName(level=SUCCESS, levelName="SUCCESS")
    logging.setLoggerClass(Logger)
    if console is None:
        console = Console(
            theme=Theme(
                styles={
                    f"logging.level.failure": Style(color="red", bold=True),
                    f"logging.level.running": Style(color="blue", bold=True),
                    f"logging.level.success": Style(color="green", bold=True),
                    f"logging.level.skipped": Style(dim=True),
                }
            )
        )
    logging.basicConfig(
        format=format,
        level=level,
        handlers=[
            RichHandler(level=level, console=console, markup=True, keywords=keywords)
        ],
    )


def get_logger(name: Optional[str] = NAME) -> Logger:
    return cast(Logger, logging.getLogger(name=name))


if __name__ == "__main__":
    install()
    logger = get_logger()
    logger.failure(message="Message")
    logger.running(message="Message")
    logger.skipped(message="Message")
    logger.success(message="Message")
