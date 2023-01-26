"""CHIME/FRB Python Logging Module."""

import logging
from datetime import datetime
from typing import Optional

import click
from rich.logging import RichHandler


# Return python logging object
def get_logger(name: Optional[str] = None, level: int = logging.INFO) -> logging.Logger:
    """Create a python logger with rich logging handler.

    Args:
        name (Optional[str], optional): Name of the module. Defaults to None.
        level (int, optional): . Defaults to logging.INFO.

    Returns:
        logging.Logger: Python logger object.
    """
    name = f"chimefrb.{name}" if name else "chimefrb"
    log = logging.getLogger(name=name)
    # Create timezone string
    tz = datetime.now().astimezone().tzinfo
    # # Detailed message format with level, module, line number, and and message
    format = "%(work_id)s%(name)s %(message)s"
    logging.basicConfig(
        level=level,
        format=format,
        datefmt=f"%d %b %Y %H:%M:%S {tz}",
        handlers=[
            RichHandler(
                level=level,
                show_path=False,
                show_time=True,
                omit_repeated_times=False,
                markup=True,
                log_time_format=f"%d %b %Y %H:%M:%S {tz}",
                show_level=True,
                rich_tracebacks=True,
                tracebacks_suppress=[click],
                tracebacks_show_locals=True,
            )
        ],
        force=True,
    )
    for handler in logging.root.handlers:
        handler.addFilter(WorkFilter(work_id=""))
    return log


class WorkFilter(logging.Filter):
    """Filter log messages by work ID."""

    def __init__(self, work_id: str) -> None:
        """Initialize the work ID.

        Args:
            work_id (str): Work ID.
        """
        self.work_id = work_id

    def filter(self, record: logging.LogRecord) -> bool:
        """Filter log messages by work ID.

        Args:
            record (logging.LogRecord): Log record.

        Returns:
            bool: True if the work ID matches the log record.
        """
        record.work_id = self.work_id
        return True


def set_work_id_for_logger(work_id: str) -> None:
    """Set the work ID for the logger.

    Args:
        work_id (str): Work ID.
    """
    for handler in logging.root.handlers:
        for filter in handler.filters:
            if isinstance(filter, WorkFilter):
                filter.work_id = work_id + " "


def unset_work_id_for_logger() -> None:
    """Unset the work ID for the logger."""
    for handler in logging.root.handlers:
        for filter in handler.filters:
            if isinstance(filter, WorkFilter):
                filter.work_id = ""
