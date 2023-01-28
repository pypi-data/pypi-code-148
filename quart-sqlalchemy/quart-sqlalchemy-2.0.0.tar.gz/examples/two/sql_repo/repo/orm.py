"""Application ORM configuration."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar
from uuid import UUID
from uuid import uuid4

from pydantic.fields import FieldInfo
from sqlalchemy import MetaData
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.event import listens_for
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry
from sqlalchemy.orm import Session
from sqlalchemy_utils import JSONType
from sqlalchemy_utils import UUIDType


# from starlite_saqlalchemy import dto, settings

BaseT = TypeVar("BaseT", bound="Base")

# DTO_KEY = "dto"
"""The key we use to reference `dto.DTOField` in the SQLAlchemy info dict."""

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
"""
Templates for automated constraint name generation.
"""


# class Mark(str, Enum):
#     """For marking column definitions on the domain models.

#     Example:
#     ```python
#     class Model(Base):
#         ...
#         updated_at: Mapped[datetime] = mapped_column(info={"dto": Mark.READ_ONLY})
#     ```
#     """

#     READ_ONLY = "read-only"
#     """To mark a field that can be read, but not updated by clients."""
#     PRIVATE = "private"
#     """To mark a field that can neither be read or updated by clients."""


@listens_for(Session, "before_flush")
def touch_updated_timestamp(session: Session, *_: Any) -> None:
    """Set timestamp on update.

    Called from SQLAlchemy's
    [`before_flush`][sqlalchemy.orm.SessionEvents.before_flush] event to bump the `updated`
    timestamp on modified instances.

    Args:
        session: The sync [`Session`][sqlalchemy.orm.Session] instance that underlies the async
            session.
    """
    for instance in session.dirty:
        instance.updated = datetime.now()


# @dataclass
# class DTOField:
#     """For configuring DTO behavior on SQLAlchemy model fields."""

#     mark: Mark | None = None
#     """Mark the field as read-only, or private."""
#     pydantic_type: Any | None = None
#     """Override the field type on the pydantic model for this attribute."""
#     pydantic_field: FieldInfo | None = None
#     """If provided, used for the pydantic model for this attribute."""
#     validators: Iterable[Callable[[Any], Any]] | None = None
#     """Single argument callables that are defined on the DTO as validators for the field."""


class Base(DeclarativeBase):
    """Base for all SQLAlchemy declarative models."""

    registry = registry(
        metadata=MetaData(naming_convention=convention),
        type_annotation_map={UUID: UUIDType, dict: JSONType},
    )

    id: Mapped[int] = mapped_column(
        default=uuid4, primary_key=True, info={"dto": DTOField(mark=Mark.READ_ONLY)}
    )
    """Primary key column."""
    created: Mapped[datetime] = mapped_column(
        default=datetime.now, info={"dto": DTOField(mark=Mark.READ_ONLY)}
    )
    """Date/time of instance creation."""
    updated: Mapped[datetime] = mapped_column(
        default=datetime.now, info={"dto": DTOField(mark=Mark.READ_ONLY)}
    )
    """Date/time of instance update."""

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        """Infer table name from class name."""
        return cls.__name__.lower()
