import datetime as dt
from pathlib import Path
from typing import Union, Literal

import pendulum
import pydantic
from pendulum import DateTime
from pydantic import BaseModel, Field, PositiveInt, PrivateAttr, validator

from script_master.settings import Settings
from script_master.template import render_template_with_variables as rndr


class BashScriptSchema(BaseModel):
    lang: Literal["bash"]
    command: list = Field(default_factory=list)  # command_line_args
    arguments: list = Field(default_factory=list)  # command_line_args
    options: dict | list = Field(default_factory=list)  # command_line_options
    env: dict = Field(default_factory=dict)
    cwd: Path | str | None = None

    def get_command_line(self) -> list:
        if isinstance(self.options, dict):
            self.options = [
                f"{'--' if not option.startswith('--') else ''}{rndr(option)}={rndr(value)}"
                for option, value in self.options.items()
            ]

        return [
            *self.command,
            *[
                f"{'-' if not arg.startswith('-') else ''}{rndr(arg)}"
                for arg in self.arguments
            ],
            *self.options,
        ]

    def get_info(self) -> dict:
        return {"command": self.get_command_line()}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GitSchema(BaseModel):
    url: str


class PythonScriptSchema(BaseModel):
    lang: Literal["python"]
    python_options: list = Field(
        default_factory=list
    )  # command_line_options for python
    python_file: str
    arguments: list = Field(default_factory=list)  # command_line_args from script
    options: dict | list = Field(
        default_factory=list
    )  # command_line_options from script
    env: dict = Field(default_factory=dict)
    cwd: Path | str | None = None

    def get_command_line(self) -> list:
        if isinstance(self.options, dict):
            self.options = [
                f"{'--' if not option.startswith('--') else ''}{rndr(option)}={rndr(value)}"
                for option, value in self.options.items()
            ]

        return [
            "{executable}",
            *self.python_options,
            self.python_file,
            *[
                f"{'-' if not arg.startswith('-') else ''}{rndr(arg)}"
                for arg in self.arguments
            ],
            *self.options,
        ]

    def get_info(self) -> dict:
        return {"command": self.get_command_line()}


class ScheduleSchema(BaseModel):
    interval: PositiveInt | Literal["daily", "hourly"]
    start_time: str | pendulum.DateTime | dt.date | dt.datetime | None
    timezone: str | None
    fill_missing: bool = False
    back_restarts: Union[pydantic.PositiveInt, list[pydantic.NegativeInt], None] = None
    _start_datetime: pendulum.DateTime | dt.datetime = PrivateAttr()
    _interval_in_seconds: int | float = PrivateAttr()

    @validator("start_time", pre=True)
    def validate_start_time(
        cls, start_time: str | pendulum.DateTime | None, values
    ) -> pendulum.DateTime:
        if (
            isinstance(start_time, pendulum.DateTime)
            and start_time.timezone_name != values["timezone"]
        ):
            start_time = start_time.astimezone(pendulum.timezone(values["timezone"]))

        elif isinstance(start_time, str):
            start_time = pendulum.parse(start_time, tz=values["timezone"])

        elif isinstance(start_time, dt.date):
            start_time = pendulum.parse(
                start_time.strftime("%Y-%m-%dT%H:%M:%S"), tz=values["timezone"]
            )

        elif isinstance(start_time, dt.datetime):
            start_time = pendulum.instance(start_time, tz=values["timezone"])

        if start_time and not isinstance(start_time, pendulum.DateTime):
            raise ValueError(f"{start_time=} is type {type(start_time)}")

        return start_time

    @validator("timezone")
    def validate_timezone(cls, timezone, values):
        if values.get("start_time") is not None and timezone is None:
            raise ValueError("If 'start_time' is present, 'timezone' is required")
        return timezone

    @validator("fill_missing")
    def validate_fill_missing(cls, fill_missing, values):
        if values.get("start_time") is None and fill_missing is True:
            raise ValueError("fill_missing cannot exist if 'start_time' is missing")
        return fill_missing

    def _set_keep_sequence(self):
        if self.start_time is not None:
            self.fill_missing = True

    def _set_interval_in_seconds(self):
        if isinstance(self.interval, (int, float)):
            self._interval_in_seconds = self.interval
        elif self.interval == "daily":
            self._interval_in_seconds = 86400
        elif self.interval == "hourly":
            self._interval_in_seconds = 3600
        else:
            raise ValueError(f"{self.interval} not supported")

    def _set_start_datetime(self):
        if self.start_time is None:
            self._start_datetime = pendulum.now(tz=self.timezone)
        else:
            self._start_datetime = self.start_time.replace(
                hour=self._start_datetime.hour,
                minute=self._start_datetime.minute,
                second=self._start_datetime.second,
            )

        if self.interval in ("daily", "hourly"):
            self._start_datetime = self._start_datetime.subtract(
                seconds=self._interval_in_seconds
            )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_interval_in_seconds()
        self._set_start_datetime()
        self._set_keep_sequence()


class WorkSchema(BaseModel):
    class ScheduleSchema(ScheduleSchema):
        ...

    schedule: ScheduleSchema
    max_retries: int = Settings().default_process_max_retries
    retry_delay: int = Settings().default_retry_delay_sec
    time_limit: int | None = None
    soft_time_limit: int = Settings().default_process_time_limit
    save_stdout: bool = False
    save_stderr: bool = True

    def get_expires(self) -> DateTime | None:
        if self.time_limit:
            expires = self.schedule._start_datetime.add(seconds=self.time_limit)
        else:
            expires = None

        return expires


class VirtualEnvSchema(BaseModel):
    version: str | None = None
    requirements: list[str] | None = Field(default_factory=list)


class NotebookSchema(BaseModel):
    class WorkSchema(WorkSchema):
        ...

    class ScriptSchemas:
        class PythonScriptSchema(PythonScriptSchema):
            ...

        class BashScriptSchema(BashScriptSchema):
            ...

    class VirtualEnvSchema(VirtualEnvSchema):
        ...

    class GitSchema(GitSchema):
        ...

    work: WorkSchema
    script: PythonScriptSchema | BashScriptSchema
    venv: VirtualEnvSchema
    git: GitSchema
