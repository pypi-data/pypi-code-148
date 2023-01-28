import datetime as dt
from typing import Optional, Any, TypeVar, Literal, Union, Iterable
from uuid import UUID

import pendulum
import pydantic
from pydantic import validator
from pydantic.generics import GenericModel
from pydantic.schema import Generic

from script_master_helper.utils import normalize_datetime
from script_master_helper.workplanner.enums import Statuses, Operators

WorkplanT = TypeVar("WorkplanT")
DataT = TypeVar("DataT")


class WorkplanManyPK(pydantic.BaseModel):
    name: pydantic.constr(max_length=100)
    worktime_utc_list: list[pendulum.DateTime]

    _worktime_utc_list = validator("worktime_utc_list", allow_reuse=True)(
        lambda wt_list: list(map(normalize_datetime, wt_list))
    )


class WorkplanPK(pydantic.BaseModel):
    name: pydantic.constr(max_length=100)
    worktime_utc: pendulum.DateTime

    _worktime_utc = validator("worktime_utc", allow_reuse=True)(normalize_datetime)


class WorkplanListGeneric(GenericModel, Generic[WorkplanT]):
    workplans: list[WorkplanT]


class Workplan(pydantic.BaseModel):
    name: pydantic.constr(max_length=100) = None
    worktime_utc: pendulum.DateTime = None
    id: UUID
    data: dict
    retries: int
    hash: str | None
    status: Statuses.LiteralT

    info: Optional[str]
    duration: Optional[int]
    expires_utc: Optional[dt.datetime]
    started_utc: Optional[dt.datetime]
    finished_utc: Optional[dt.datetime]
    created_utc: pendulum.DateTime
    updated_utc: pendulum.DateTime

    _expires_utc = validator("expires_utc", allow_reuse=True)(normalize_datetime)
    _started_utc = validator("started_utc", allow_reuse=True)(normalize_datetime)
    _finished_utc = validator("finished_utc", allow_reuse=True)(normalize_datetime)
    _created_utc = validator("created_utc", allow_reuse=True)(normalize_datetime)
    _updated_utc = validator("updated_utc", allow_reuse=True)(normalize_datetime)

    class Config:
        orm_mode = True

    @classmethod
    def list_from_orm(cls, result: Iterable) -> list["Workplan"]:
        return [cls.from_orm(obj) for obj in result]


class WorkplanUpdate(pydantic.BaseModel):
    name: pydantic.constr(max_length=100) = None
    worktime_utc: pendulum.DateTime = None
    id: UUID = None
    data: dict = None
    retries: int = None
    hash: str | None = None
    status: Statuses.LiteralT = None
    info: Optional[str] = None
    duration: int | None = None
    expires_utc: Optional[dt.datetime] = None
    started_utc: Optional[dt.datetime] = None
    finished_utc: Optional[dt.datetime] = None

    _expires_utc = validator("expires_utc", allow_reuse=True)(normalize_datetime)
    _started_utc = validator("started_utc", allow_reuse=True)(normalize_datetime)
    _finished_utc = validator("finished_utc", allow_reuse=True)(normalize_datetime)
    _worktime_utc = validator("worktime_utc", allow_reuse=True)(normalize_datetime)

    @validator("id")
    def validate_id(cls, id, values, **kwargs):
        if not id:
            if not values["name"] or not values["worktime_utc"]:
                raise ValueError("'id' field or fields ('name', 'worktime_utc') are required")

        return id


class WorkplanFields(pydantic.BaseModel):
    field_names: list[
        Literal[
            "id",
            "name",
            "worktime_utc",
            "data",
            "retries",
            "duration",
            "hash",
            "status",
            "info",
            "expires_utc",
            "started_utc",
            "finished_utc",
            "created_utc",
            "updated_utc",
        ]
    ] = None


class WorkplanExtraData(pydantic.BaseModel):
    status: Statuses.LiteralT = Statuses.default
    max_retries: int = 0
    hash: str = None
    expires_utc: Optional[pendulum.DateTime] = None
    info: str = None
    data: dict = pydantic.Field(default_factory=dict)


class GenerateWorkplans(pydantic.BaseModel):
    class Extra(WorkplanExtraData):
        ...

    name: str
    start_time: pendulum.DateTime
    interval_in_seconds: Union[int, float] = None
    keep_sequence: bool = False
    retry_delay: int = 60
    max_fatal_errors: int = 3
    back_restarts: Union[pydantic.PositiveInt, list[pydantic.NegativeInt], None] = None
    extra: Extra = pydantic.Field(default_factory=Extra)

    @validator("start_time", allow_reuse=True)
    def validate_start_time(cls, value):
        dt_ = normalize_datetime(value)
        if dt_.second != 0 or dt_.microsecond != 0:
            raise ValueError("Param of 'start_time' should be shortened to minutes")

        return dt_

    @property
    def interval_timedelta(self):
        return dt.timedelta(seconds=self.interval_in_seconds)


class GenerateChildWorkplans(pydantic.BaseModel):
    class Extra(WorkplanExtraData):
        ...

    name: str
    parent_name: str = None
    status_trigger: str = None
    extra: Extra = pydantic.Field(default_factory=Extra)


class Error(pydantic.BaseModel):
    code: int
    message: str
    detail: Any = None

    def __eq__(self, other):
        return other.code == self.code and getattr(other, "message", getattr(other, "detail")) == self.message


class ResponseGeneric(GenericModel, Generic[DataT]):
    """https://pydantic-docs.helpmanual.io/usage/models/#generic-models"""

    data: Optional[DataT] = None
    error: Optional[Error] = None

    @validator("error", always=True)
    def check_consistency(cls, error, values):
        if error is not None and values["data"] is not None:
            raise ValueError("must not provide both data and error")
        if error is None and values.get("data") is None:
            raise ValueError("must provide data or error")
        return error


class Affected(pydantic.BaseModel):
    count: int


class FieldFilterGeneric(GenericModel, Generic[DataT]):
    """https://pydantic-docs.helpmanual.io/usage/models/#generic-models"""

    value: DataT
    operator: Operators.LiteralT = None

    @validator("operator")
    def validate_operator(cls, operator, values, **kwargs):
        if operator is None and isinstance(values["value"], (list, tuple, set)):
            return Operators.in_
        elif operator is None:
            return Operators.equal
        else:
            return operator


StringFilterT = FieldFilterGeneric[Union[str, list[str]]]
UUIDFilterT = FieldFilterGeneric[Union[UUID, list[UUID]]]
IntFilterT = FieldFilterGeneric[int]
OptionalIntFilterT = FieldFilterGeneric[Optional[int]]
DateTimeFilterT = FieldFilterGeneric[dt.datetime]
OptionalDateTimeFilterT = FieldFilterGeneric[Optional[dt.datetime]]
JsonFilterT = FieldFilterGeneric[Union[str, dict, list]]


class _WorkplanQueryFilter(pydantic.BaseModel):
    id: list[UUIDFilterT] = None
    name: list[StringFilterT] = None
    worktime_utc: list[DateTimeFilterT] = None
    data: list[JsonFilterT] = None
    retries: list[IntFilterT] = None
    hash: list[StringFilterT] = None
    status: list[FieldFilterGeneric[Statuses.LiteralT]] = None
    info: list[StringFilterT] = None
    expires_utc: list[OptionalDateTimeFilterT] = None
    started_utc: list[OptionalDateTimeFilterT] = None
    finished_utc: list[OptionalDateTimeFilterT] = None
    created_utc: list[DateTimeFilterT] = None
    updated_utc: list[DateTimeFilterT] = None

    _worktime_utc = validator("worktime_utc", allow_reuse=True)(normalize_datetime)
    _expires_utc = validator("expires_utc", allow_reuse=True)(normalize_datetime)
    _started_utc = validator("started_utc", allow_reuse=True)(normalize_datetime)
    _finished_utc = validator("finished_utc", allow_reuse=True)(normalize_datetime)
    _updated_utc = validator("updated_utc", allow_reuse=True)(normalize_datetime)
    _created_utc = validator("created_utc", allow_reuse=True)(normalize_datetime)


class WorkplanQuery(pydantic.BaseModel):
    class Filter(_WorkplanQueryFilter):
        ...

    class Value(FieldFilterGeneric):
        ...

    filter: Filter
    order_by: list[
        Literal[
            "id",
            "name",
            "worktime_utc",
            "data",
            "retries",
            "duration",
            "hash",
            "status",
            "info",
            "expires_utc",
            "started_utc",
            "finished_utc",
            "created_utc",
            "updated_utc",
        ]
    ] = None
    limit: int = None
    page: int = None

    @validator("page")
    def validate_page(cls, page, values):
        if page is not None and values["limit"] is None:
            raise ValueError("If PAGE is present, the LIMIT field is required")
