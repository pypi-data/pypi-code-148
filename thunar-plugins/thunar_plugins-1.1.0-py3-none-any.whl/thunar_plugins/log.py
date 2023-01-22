# system modules
import os
import logging

# internal modules

# external modules
import rich
from rich.logging import RichHandler
from rich.console import Console

loglevel = (
    os.environ.get("THUNAR_PLUGINS_LOGLEVEL", "warning").upper() or "WARNING"
)

console = Console()

logging.basicConfig(
    level=loglevel
    if loglevel in {"NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    else "notset",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)],
)
