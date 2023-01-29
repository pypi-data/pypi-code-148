import os
import sys
from pathlib import Path

SETTINGS_FILENAME = ".env"
HOME_DIR_VARNAME = "PROCESS_EXECUTOR_HOME"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8082
DEFAULT_DEBUG = False
DEFAULT_LOGLEVEL = "INFO"
DEFAULT_LOGS_ROTATION = "1 day"  # Once the file is too old, it's rotated
DEFAULT_LOGS_RETENTION = "1 months"  # Cleanup after some time
HEARBEAT_INTERVAL_SEC: int = 5
MAX_PROCESSES = (os.cpu_count() or 2) * 4
DEFAULT_PYTHON_VERSION = ".".join(sys.version.split(".")[:2])
DEFAULT_PIP_PACKAGES = ("pip", "setuptools==57.5.0", "wheel")
DEFAULT_PROCESS_TIMEOUT_SEC = 3600


def get_homepath() -> Path:
    try:
        return Path(os.environ[HOME_DIR_VARNAME])
    except KeyError:
        if os.environ.get("PYTEST") or Path().cwd().name == "tests":
            return Path("NotImplemented")
        elif Path(SETTINGS_FILENAME) in Path().glob("*"):
            return Path().cwd()

        raise
