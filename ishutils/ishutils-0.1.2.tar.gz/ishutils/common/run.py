import shlex
import subprocess
from pathlib import Path
from typing import Sequence

from ..logging import Logger, get_logger

__all__: list[str] = ["run"]


def run(args: Sequence[str | Path], *run_args, **kwargs) -> subprocess.CompletedProcess:
    logger: Logger = get_logger()
    logger.running(message="+ " + shlex.join(list(map(str, args))))
    return subprocess.run(args=args, *run_args, **kwargs)
