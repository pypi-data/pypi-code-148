from typing import Any, Sequence, Union, Optional

from alembic.runtime.migration import MigrationContext
from alembic.operations import Operations

# TODO: replace with interfaces
from sqlalchemy import Table, Column
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session

from sqlalchemize.features import get_table, get_primary_key_constraints
from sqlalchemize.insert import insert_from_table
from sqlalchemize.drop import drop_table
from sqlalchemize.type_convert import sql_type


def _get_op(
    engine: Engine
) -> Operations:
    conn = engine.connect()
    ctx = MigrationContext.configure(conn)
    return Operations(ctx)


def rename_column(
    table_name: str,
    old_col_name: str,
    new_col_name: str,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Renames a table column.

        Returns newly reflected SqlAlchemy Table.
    """
    op = _get_op(engine)
    
    with op.batch_alter_table(table_name, schema=schema) as batch_op:
        batch_op.alter_column(old_col_name, nullable=True, new_column_name=new_col_name)  # type: ignore
    return get_table(table_name, engine, schema=schema)


def drop_column(
    table_name: str,
    col_name: str,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Drops a table column.

        Returns newly reflected SqlAlchemy Table.
    """
    op = _get_op(engine)
    with op.batch_alter_table(table_name, schema=schema) as batch_op:
        batch_op.drop_column(col_name)  # type: ignore
    return get_table(table_name, engine, schema=schema)


def add_column(
    table_name: str,
    column_name: str,
    dtype: Any,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    sa_type = sql_type(dtype)
    op = _get_op(engine)
    col = Column(column_name, sa_type)
    op.add_column(table_name, col, schema=schema)  # type: ignore
    return get_table(table_name, engine, schema=schema)


def rename_table(
    old_table_name: str,
    new_table_name: str,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Renames a table.

        Returns newly reflected SqlAlchemy Table.
    """
    op = _get_op(engine)
    op.rename_table(old_table_name, new_table_name, schema=schema)  # type: ignore
    return get_table(new_table_name, engine, schema=schema)


def copy_table(
    table: Table,
    new_table_name: str,
    engine: Engine,
    if_exists: str = 'replace',
    schema: Optional[str] = None
) -> Table:
    """
        Creates a copy of the given table with new_table_name.
        Drops a table with same new_table_name if_exists='replace'

        Returns the new SqlAlchemy Table.
    """
    op = _get_op(engine)
    if if_exists == 'replace':
        drop_table(new_table_name, engine, schema=schema)
    op.create_table(new_table_name, *table.c, table.metadata, schema=schema)  # type: ignore
    new_table = get_table(new_table_name, engine, schema=schema)
    insert_from_table(table, new_table, engine)
    return new_table


def replace_primary_key(
    table: Table,
    column_name: str,
    engine: Engine,
    schema: Optional[str] = None
)-> Table:
    """
        Drops primary key from table columns
        then adds primary key to column_name of table.

        Returns newly reflected SqlAlchemy Table.
    """
    return replace_primary_keys(table, [column_name], engine, schema)


def replace_primary_keys(
    table: Table,
    column_names: Sequence[str],
    engine: Engine,
    schema: Optional[str] = None
)-> Table:
    """
        Drops primary key from table columns
        then adds primary key to column_name of table.

        Returns newly reflected SqlAlchemy Table.
    """
    table_name = table.name
    op = _get_op(engine)
    keys = get_primary_key_constraints(table)
    
    with op.batch_alter_table(table_name, schema=schema) as batch_op:
        # name primary key constraint if not named (sqlite)
        if keys[0] is None:
            constraint_name = f'pk_{table_name}'
            batch_op.create_primary_key(constraint_name, keys[1])  # type: ignore
        else:
            constraint_name = keys[0]
        batch_op.drop_constraint(constraint_name, type_='primary')  # type: ignore
        batch_op.create_unique_constraint(constraint_name, column_names)  # type: ignore
        batch_op.create_primary_key(constraint_name, column_names)  # type: ignore
    return get_table(table_name, engine)


def create_primary_key(
    table_name: str,
    column_name: str,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Adds a primary key constraint to table.
        Only use on a table with no primary key.
        Use replace_primary_key on tables with a primary key.

        Returns newly reflected SqlAlchemy Table.
    """
    return create_primary_keys(table_name, [column_name], engine, schema)


def create_primary_keys(
    table_name: str,
    column_names: Sequence[str],
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Adds a primary key constraint to table.
        Only use on a table with no primary key.
        Use replace_primary_key on tables with a primary key.

        Returns newly reflected SqlAlchemy Table.
    """
    op = _get_op(engine)
    constraint_name = f'pk_{table_name}'
    with op.batch_alter_table(table_name, schema=schema) as batch_op:
        batch_op.create_unique_constraint(constraint_name, column_names)  # type: ignore
        batch_op.create_primary_key(constraint_name, column_names)  # type: ignore
    return get_table(table_name, engine, schema=schema)


def name_primary_key(
    table_name: str,
    column_name: str,
    engine: Engine,
    schema: Optional[str] = None
) -> Table:
    """
        Names the primary key constraint for a given sql table column.

        Returns newly reflected SqlAlchemy Table.
    """
    create_primary_key(table_name, column_name, engine, schema=schema)
    return get_table(table_name, engine, schema=schema)