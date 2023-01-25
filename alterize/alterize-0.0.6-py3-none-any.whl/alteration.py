from dataclasses import dataclass
from typing import Any, Optional, Protocol

from sqlalchemy.engine import Engine
import sqlalchemy.orm.session as sa_session
import sqlalchemy as sa
from sqlalchemize.features import get_column_types, get_table
from sqlalchemize.type_convert import _sql_to_python
from sqlalchemize.update import update_records
from sqlalchemize.drop import drop_table

import alterize as alt
from alterize.update import set_column_values_session


class Alteration(Protocol):
    def upgrade(self) -> sa.Table:
        ...

    def downgrade(self) -> sa.Table:
        ...


@dataclass
class RenameColumn(Alteration):
    table_name: str
    old_col_name: str
    new_col_name: str
    engine: Engine
    schema: Optional[str] = None

    def upgrade(self) -> sa.Table:
        return alt.rename_column(
            self.table_name,
            self.old_col_name,
            self.new_col_name,
            self.engine,
            self.schema
        )

    def downgrade(self) -> sa.Table:
        return alt.rename_column(
            self.table_name,
            self.new_col_name,
            self.old_col_name,
            self.engine,
            self.schema
        )


@dataclass
class DropColumn(Alteration):
    table_name: str
    col_name: str
    engine: Engine
    schema: Optional[str] = None

    def upgrade(self) -> sa.Table:
        table = get_table(self.table_name, self.engine, self.schema)
        self.dtype = _sql_to_python[type(get_column_types(table)[self.col_name])]
        self.table_copy = alt.copy_table(table, f'%copy%{self.table_name}', self.engine, schema=self.schema)
        return alt.drop_column(
            self.table_name,
            self.col_name,
            self.engine,
            self.schema
        )

    def downgrade(self) -> sa.Table:
        return alt.add_column(
            self.table_name,
            self.col_name,
            self.dtype,
            self.engine,
            self.schema
        )
        # TODO: add back column values


@dataclass
class AddColumn(Alteration):
    table_name: str
    column_name: str
    dtype: Any
    engine: Engine
    schema: Optional[str] = None

    def upgrade(self) -> sa.Table:
        return alt.add_column(
            self.table_name,
            self.column_name,
            self.dtype,
            self.engine,
            self.schema
        )

    def downgrade(self) -> sa.Table:
        return alt.drop_column(
            self.table_name,
            self.column_name,
            self.engine,
            self.schema
        )

    
@dataclass
class RenameTable(Alteration):
    old_table_name: str
    new_table_name: str
    engine: Engine
    schema: Optional[str] = None

    def upgrade(self) -> sa.Table:
        return alt.rename_table(
            self.old_table_name,
            self.new_table_name,
            self.engine,
            self.schema
        )

    def downgrade(self) -> sa.Table:
        return alt.rename_table(
            self.new_table_name,
            self.old_table_name,
            self.engine,
            self.schema
        )


@dataclass
class CopyTable(Alteration):
    table: sa.Table
    new_table_name: str
    engine: Engine
    if_exists: str = 'replace'
    schema: Optional[str] = None

    def upgrade(self) -> sa.Table:
        table_copy = alt.copy_table(
            self.table,
            self.new_table_name,
            self.engine,
            self.if_exists,
            self.schema,
        )
        return table_copy

    def downgrade(self) -> sa.Table:
        table_copy = get_table(self.new_table_name, self.engine, self.schema)
        drop_table(
            table_copy,
            self.engine,
            schema=self.schema
        )
        return self.table