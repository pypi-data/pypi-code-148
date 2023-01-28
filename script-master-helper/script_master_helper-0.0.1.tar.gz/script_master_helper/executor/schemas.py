import datetime as dt
from typing import TypeVar, Any
from uuid import UUID

from pydantic import BaseModel, validator, Field
from pydantic.generics import GenericModel
from pydantic.schema import Generic

DataT = TypeVar("DataT")


class Error(BaseModel):
    code: int
    message: str
    detail: Any = None

    def __eq__(self, other):
        return other.code == self.code and getattr(other, "message", getattr(other, "detail")) == self.message


class ResponseGenericSchema(GenericModel, Generic[DataT]):
    """https://pydantic-docs.helpmanual.io/usage/models/#generic-models"""

    data: DataT | None = None
    error: Error | None = None

    @validator("error", always=True)
    def check_consistency(cls, error, values):
        if error is not None and values["data"] is not None:
            raise ValueError("must not provide both data and error")
        if error is None and values.get("data") is None:
            raise ValueError("must provide data or error")

        return error


class GitSchema(BaseModel):
    url: str

    def get_repo_name(self):
        return self.url.split('/')[-1].split('.')[0].replace('-', '_')


class VirtualEnvSchema(BaseModel):
    version: str | None = None
    requirements: list[str]


class ProcessCreateSchema(BaseModel):
    class GitSchema(GitSchema):
        ...
    class VirtualEnvSchema(VirtualEnvSchema):
        ...

    workplan_id: UUID | str
    name: str = ""
    command: list
    git: GitSchema
    venv: VirtualEnvSchema
    time_limit: int | float
    expires_utc: dt.datetime | None = None
    cwd: str | None = None
    env: dict = Field(default_factory=dict)
    subprocess_kwargs: dict = Field(default_factory=dict)
    save_stdout: bool = False
    save_stderr: bool = True

    def get_timeout(self) -> int | float:
        if self.expires_utc is None:
            return self.time_limit
        else:
            return (self.expires_utc - dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)).total_seconds()


class ProcessDataSchema(ProcessCreateSchema):
    id: str
    pid: int | None
    is_done: bool
    has_error: bool
    error_message: str | None
    started_utc: dt.datetime | None
    finished_utc: dt.datetime | None


class ProcessCreateResponseSchema(BaseModel):
    id: str
