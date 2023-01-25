from typing import Any, Optional, Protocol

from sqlalchemy.engine import Engine
import sqlalchemy as sa
from alembic.operations import Operations

from alterize.alter import _get_op
from alterize.alteration import AddColumn, CopyTable, DropColumn, RenameColumn, RenameTable


class Alteration(Protocol):
    def upgrade(self) -> sa.Table:
        ...

    def downgrade(self) -> sa.Table:
        ...


class Migration:
    """Keep track of alterations and allow rollback of changes."""
    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._upgrades: list[Alteration] = []
        self._downgrades: list[Alteration] = []

    @property
    def _op(self) -> Operations:
        return _get_op(self._engine)

    def _add_upgrade(self, alteration: Alteration) -> None:
        self._upgrades.append(alteration)

    def _add_downgrade(self, alteration: Alteration) -> None:
        self._downgrades.append(alteration)

    def upgrade(self) -> sa.Table:
        for i, alteration in enumerate(list(self._upgrades)):
            table = alteration.upgrade()
            self._add_downgrade(alteration)
            del self._upgrades[i]
        return table

    def downgrade(self) -> sa.Table:
        for i, alteration in enumerate(list(self._downgrades)):
            table = alteration.downgrade()
            del self._downgrades[i]
        return table

    def rename_column(
        self,
        table_name: str,
        old_col_name: str,
        new_col_name: str,
        engine: Engine,
        schema: Optional[str] = None
    ) -> None:
        alteration = RenameColumn(
            table_name,
            old_col_name,
            new_col_name,
            engine,
            schema
        )
        self._add_upgrade(alteration)

    def drop_column(
        self,
        table_name: str,
        col_name: str,
        engine: Engine,
        schema: Optional[str] = None
    ) -> None:
        alteration = DropColumn(
            table_name,
            col_name,
            engine,
            schema
        )
        self._add_upgrade(alteration)

    def add_column(
        self,
        table_name: str,
        column_name: str,
        dtype: Any,
        engine: Engine,
        schema: Optional[str] = None
    ) -> None:
        alteration = AddColumn(
            table_name,
            column_name,
            dtype,
            engine,
            schema
        )
        self._add_upgrade(alteration)

    def rename_table(
        self,
        old_table_name: str,
        new_table_name: str,
        engine: Engine,
        schema: Optional[str] = None
    ) -> None:
        alteration = RenameTable(
            old_table_name,
            new_table_name,
            engine,
            schema
        )
        self._add_upgrade(alteration)

    def copy_table(
        self,
        table: sa.Table,
        new_table_name: str,
        engine: Engine,
        if_exists: str = 'replace',
        schema: Optional[str] = None
    ) -> None:
        alteration = CopyTable(
            table,
            new_table_name,
            engine,
            if_exists,
            schema
        )
        self._add_upgrade(alteration)
    