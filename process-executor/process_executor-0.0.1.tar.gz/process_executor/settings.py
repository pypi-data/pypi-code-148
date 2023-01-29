from pathlib import Path
from process_executor.app import logger

from confz import ConfZ, ConfZFileSource, ConfZEnvSource, ConfZCLArgSource
from pydantic import validator

from process_executor import const


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
    hearbeat_interval_sec: int = const.HEARBEAT_INTERVAL_SEC
    max_processes: int = const.MAX_PROCESSES
    default_python_version: str = const.DEFAULT_PYTHON_VERSION
    default_pip_packages: list | tuple = const.DEFAULT_PIP_PACKAGES
    default_process_timeout_sec: int = const.DEFAULT_PROCESS_TIMEOUT_SEC

    workplanner_host: str
    workplanner_port: int = None

    CONFIG_SOURCES = [
        ConfZEnvSource(
            allow_all=True, file=const.get_homepath() / const.SETTINGS_FILENAME
        ),
        ConfZEnvSource(
            allow_all=True,
            prefix="EXECUTOR_",
            file=const.get_homepath() / const.SETTINGS_FILENAME,
        ),
        ConfZFileSource(
            optional=True,
            file_from_cl="--settings-file",
            file_from_env="EXECUTOR_SETTINGS_FILE",
        ),
        ConfZCLArgSource(),
    ]

    @validator("loglevel")
    def validate_loglevel(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @validator("default_pip_packages")
    def validate_default_pip_packages(cls, value):
        if isinstance(value, str):
            return tuple(value.split())

        return value

    @property
    def scripts_dir(self) -> Path:
        return Path(const.get_homepath() / "scripts")

    @property
    def logs_dir(self) -> Path:
        return Path(const.get_homepath() / "logs")

    @property
    def process_log_dir(self):
        return const.get_homepath() / "logs" / "processes"

    @property
    def logpath(self):
        return const.get_homepath() / "logs" / "executor.log"

    @property
    def error_log_path(self):
        return const.get_homepath() / "logs" / "executor.error.log"

    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
