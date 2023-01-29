import os
import pathlib
from os.path import abspath
from pathlib import Path

from starlette.templating import Jinja2Templates

SETTINGS_FILENAME = ".env"
HOME_DIR_VARNAME = "SCRIPT_MASTER_HOME"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8083
DEFAULT_DEBUG = False
DEFAULT_LOGLEVEL = "INFO"
templates = Jinja2Templates(
    directory=str(pathlib.Path(abspath(__file__)).parent / "templates")
)


def get_homepath() -> Path:
    try:
        return Path(os.environ[HOME_DIR_VARNAME])
    except KeyError:
        if os.environ.get("PYTEST") or Path().cwd().name == "tests":
            return Path("NotImplemented")
        elif Path(SETTINGS_FILENAME) in Path().glob("*"):
            return Path().cwd()

        raise
