from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class HasId:
    """Mixin that adds an ``id`` column to a model.

    The column is an integer primary key that is auto-incremented.
    """

    id: Mapped[int] = mapped_column(primary_key=True)


class HasTimestamps:
    """Mixin that adds ``created_at`` and ``updated_at`` columns to a model.

    The columns are ``DateTime`` columns that default to the current time.
    """

    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False, onupdate=func.now()
    )


class SoftDelete:
    """Mixin that adds a ``deleted_at`` column to a model.

    The column is a ``DateTime`` column that defaults to ``NULL``.
    """

    deleted_at: Mapped[Optional[datetime]] = mapped_column(default=func.now())

    @property
    def is_active(self):
        return self.deleted_at is None


class HasVersion:
    """Mixin that adds a ``version`` column to a model.

    The column is an integer column that defaults to ``0``.
    """

    version: Mapped[int] = mapped_column(default=0)

    @declared_attr.directive
    def __mapper_args__(cls) -> Mapping[str, Any]:
        return dict(version_id_col=cls.version)


class HasVerified:
    """Mixin that adds a ``verified_at`` column to a model.

    The column is an datetime column that defaults to None.
    """

    verified_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    @property
    def is_verified(self):
        return self.verified_at is not None

    def verify_model(self):
        self.verified_at = datetime.now()


class Consumable:
    """Mixin that adds a ``consumed_at`` column to a model.

    The column is an datetime column that defaults to None.
    """

    consumed_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    @property
    def is_consumed(self):
        return self.consumed_at is not None

    def consume_model(self):
        self.consumed_at = datetime.now()


class Revokable:
    """Mixin that adds a ``revoked_at`` column to a model.

    The column is an datetime column that defaults to None.
    """

    revoked_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    @property
    def is_revoked(self):
        return self.revoked_at is not None

    def revoke_model(self):
        self.revoked_at = datetime.now()


class HasExpiration:
    """Mixin that adds a ``expires_at`` column to a model.

    The column is an datetime column.
    """

    expires_at: Mapped[datetime] = mapped_column()

    @property
    def is_expired(self):
        return datetime.now() >= self.expires_at
