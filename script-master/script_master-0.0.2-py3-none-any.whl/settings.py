import os
from pathlib import Path

from aiopath import AsyncPath
from confz import ConfZ, ConfZFileSource, ConfZEnvSource, ConfZCLArgSource
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
    logs_rotation: str = const.DEFAULT_LOGS_ROTATION
    logs_retention: str = const.DEFAULT_LOGS_RETENTION
    default_process_time_limit: int = const.DEFAULT_PROCESS_TIME_LIMIT
    default_process_max_retries: int = const.DEFAULT_PROCESS_MAX_RETRIES
    default_retry_delay_sec: int = const.DEFAULT_RETRY_DELAY_SEC
    hearbeat_interval_sec: int = const.HEARBEAT_INTERVAL_SEC

    workplanner_host: str
    workplanner_port: int = None
    executor_host: str
    executor_port: int = None

    CONFIG_SOURCES = [
        ConfZEnvSource(
            allow_all=True, file=const.get_homepath() / const.SETTINGS_FILENAME
        ),
        ConfZEnvSource(
            allow_all=True,
            prefix="SCRIPT_MASTER_",
            file=const.get_homepath() / const.SETTINGS_FILENAME,
        ),
        ConfZFileSource(
            optional=True,
            file_from_cl="--settings-file",
            file_from_env="SCRIPT_MASTER_SETTINGS_FILE",
        ),
        ConfZCLArgSource(),
    ]

    @validator("loglevel")
    def validate_loglevel(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @property
    def VARIABLES_DIR(self) -> AsyncPath:
        return AsyncPath(const.get_homepath() / "variables")

    @property
    def NOTEBOOK_DIR(self) -> AsyncPath:
        return AsyncPath(const.get_homepath() / "notebooks")

    @property
    def ARCHIVE_NOTEBOOK_DIR(self) -> AsyncPath:
        return AsyncPath(const.get_homepath() / "notebooks" / "__archive__")

    @property
    def LOGS_DIR(self) -> AsyncPath:
        return AsyncPath(const.get_homepath() / "logs")

    def __init__(self, **kwargs):
        if os.environ.get("PYTEST") or Path().cwd().name == "tests":
            kwargs.setdefault("workplanner_host", "NotImplemented")
            kwargs.setdefault("executor_host", "NotImplemented")

        super().__init__(**kwargs)
