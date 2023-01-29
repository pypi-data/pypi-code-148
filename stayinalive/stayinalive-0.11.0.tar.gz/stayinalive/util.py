import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENCODING = "utf-8"

TESTS_DIRECTORY_DEFAULT = "/etc/stayinalive"
MODE_FILE_DEFAULT = "/var/stayinalive/mode"
STATUS_FILE_DEFAULT = "/var/stayinalive/status.json"
DELAY_DEFAULT = 10

FIXING = "fixing"
OK = "ok"
KO = "ko"
TEST = "test"
ORDER = "order"
MODE = "mode"
FIX = "fix"
TIMESTAMP = "timestamp"
STATUS = "status"
INIT = "init"

SP_KWARGS = {"stdout": subprocess.PIPE, "stderr": subprocess.STDOUT, "encoding": ENCODING}  # common parameters to subprocess commands


def print_output(command: str, result: str, output: Any, prefix: str) -> None:
    """
    Provides a standard way to print the output of a command's execution.

    :param command: obviously
    :param result: describes the outcome of the command's execution
    :param output: execution's output lines
    :param prefix: prepended to all printed lines
    """

    print(prefix, result + ":", command)
    for line in output:
        print(prefix, "output:", line.rstrip())


def write(file: Path, mode: str, status: str, timestamp: float = None) -> None:
    """
    Writes the given timestamp, status and mode into a JSON file.

    :param file: Path to the target file
    :param mode: mode
    :param status: status
    :param timestamp: timestamp, defaults to the current timestamp
    """

    if timestamp is None:  # fix: can't put directly time.time() as a default value (see https://stackoverflow.com/questions/1132941)
        timestamp = time.time()

    file.write_text(
        json.dumps(
            {
                TIMESTAMP: datetime.fromtimestamp(timestamp, timezone.utc).isoformat(),
                STATUS: status,
                MODE: mode
            }, indent=2
        ), encoding=ENCODING  # todo: can't seem to be able to properly test the encoding
    )


def is_ko(file: Path) -> bool:
    f"""
    :param file: Path to the target file
    :return: whether the file explicitly mentions a {KO} status or not
    """

    try:
        return json.loads(file.read_text(encoding=ENCODING)).get(STATUS) == KO
    except (OSError, ValueError):
        return False
