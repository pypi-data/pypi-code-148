from aiopath import AsyncPath
from confz import ConfZ, ConfZFileSource, ConfZEnvSource, ConfZCLArgSource
from pathlib import Path
from pydantic import validator
from script_master import const


class Settings(ConfZ):
    """
    Typer (CLI) replaces "_" characters in parameters with "-", so you need to write parameters without using "_",
    otherwise ConfZ will not see them.

    ConfZ converts ENV variables to lowercase, so lowercase must also be used in the config.
    """

    host: str = const.DEFAULT_HOST
    port: int = const.DEFAULT_PORT
    debug: bool = const.DEFAULT_DEBUG
    loglevel: str = const.DEFAULT_LOGLEVEL

    workplanner_host: str
    workplanner_port: int = None

    CONFIG_SOURCES = [
        ConfZFileSource(
            optional=True,
            file_from_cl="--settings-file",
            file_from_env="SCRIPT_MASTER_SETTINGS_FILE",
        ),
        ConfZEnvSource(
            allow_all=True, file=const.get_homepath() / const.SETTINGS_FILENAME
        ),
        ConfZEnvSource(
            allow_all=True,
            prefix="SCRIPT_MASTER_UI_",
            file=const.get_homepath() / const.SETTINGS_FILENAME,
        ),
        ConfZCLArgSource(),
    ]

    @validator("loglevel")
    def validate_loglevel(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
