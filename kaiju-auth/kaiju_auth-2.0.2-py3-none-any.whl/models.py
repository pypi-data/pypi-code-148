"""Database table schemas for permissions, users, groups etc.

Relation diagram
----------------

.. image:: ../images/users_and_groups_erd.png

Usage
-----

You can create custom tables by invoking specific functions in your project.

.. code-block:: python

    meta = sa.MetaData()
    permissions = create_permissions_table(
        'permissions', meta,
        sa.Column('custom_column', sa.TEXT)  # custom column
    )


Functions
---------

"""

from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

__all__ = (
    'create_permissions_table',
    'permissions',
    'create_groups_table',
    'groups',
    'create_group_permissions_table',
    'group_permissions',
    'create_users_table',
    'users',
    'create_user_groups_table',
    'user_groups',
    'create_sessions_table',
    'sessions',
)


def create_permissions_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """Get permissions table.

    :param table_name: custom table name
    :param metadata: custom metadata object
    :param columns: additional columns
    """
    _table = sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
        sa.Column('enabled', sa.Boolean, nullable=False, default=True),
        sa.Column('tag', sa.TEXT, nullable=True),
        sa.Column('description', sa.TEXT, nullable=True),
        *columns,
    )
    return _table


def create_groups_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """Get group table.

    :param table_name: custom table name
    :param role_table_name: name of the roles table
    :param metadata: custom metadata object
    :param columns: additional columns
    """
    _table = sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
        sa.Column('tag', sa.TEXT, nullable=True),
        sa.Column('description', sa.TEXT, nullable=True),
        *columns,
    )
    return _table


def create_group_permissions_table(
    table_name: str, groups_table_name: str, permissions_table_name: str, metadata: sa.MetaData, *columns: sa.Column
):
    """Get group permissions table.

    :param table_name: custom table name
    :param permissions_table_name:
    :param groups_table_name:
    :param metadata: custom metadata object
    :param columns: additional columns
    """
    _table = sa.Table(
        table_name,
        metadata,
        sa.Column(
            'group_id', sa.ForeignKey(f'{groups_table_name}.id', ondelete='CASCADE'), nullable=False, primary_key=True
        ),
        sa.Column(
            'permission_id',
            sa.ForeignKey(f'{permissions_table_name}.id', ondelete='CASCADE'),
            nullable=False,
            primary_key=True,
        ),
        *columns,
    )
    return _table


def create_users_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column, **kwargs):
    """Get users table.

    :param table_name: custom table name
    :param metadata: custom metadata object
    :param columns: additional columns
    :param kwargs: additional table params
    """
    _users = sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa_pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
        sa.Column('username', sa.TEXT, unique=True, nullable=False),
        sa.Column('email', sa.TEXT, unique=True, nullable=False),
        sa.Column('full_name', sa.TEXT, nullable=True),
        sa.Column('password', sa_pg.BYTEA, nullable=False),
        sa.Column('salt', sa_pg.BYTEA, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False, default=True),
        sa.Column('is_blocked', sa.Boolean, nullable=False, default=False),
        sa.Column(
            'created',
            sa.DateTime,
            nullable=False,
            default=datetime.utcnow,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp()),
        ),
        sa.Column('settings', sa_pg.JSONB, nullable=False, default={}, server_default=sa.text("'{}'::jsonb")),
        *columns,
        **kwargs,
    )
    return _users


def create_user_groups_table(
    table_name: str, groups_table_name: str, users_table_name: str, metadata: sa.MetaData, *columns: sa.Column
):
    """Get user-group table.

    :param table_name: custom table name
    :param groups_table_name:
    :param users_table_name:
    :param metadata: custom metadata object
    :param columns: additional columns
    """
    _table = sa.Table(
        table_name,
        metadata,
        sa.Column(
            'group_id', sa.ForeignKey(f'{groups_table_name}.id', ondelete='CASCADE'), nullable=False, primary_key=True
        ),
        sa.Column(
            'user_id', sa.ForeignKey(f'{users_table_name}.id', ondelete='CASCADE'), nullable=False, primary_key=True
        ),
        *columns,
    )
    return _table


def create_sessions_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """Create session table.

    :param table_name: custom table name
    :param metadata: custom metadata object
    :param columns: additional columns
    """
    return sa.Table(
        table_name,
        metadata,
        sa.Column('id', sa_pg.UUID(as_uuid=True), primary_key=True),
        sa.Column('created', sa.TIMESTAMP, nullable=False),
        sa.Column('data', sa_pg.JSONB, nullable=False),
        sa.Column('expires', sa.TIMESTAMP, nullable=False),
        *columns,
    )


meta = sa.MetaData()
permissions = create_permissions_table('permissions', meta)
groups = create_groups_table('groups', meta)
group_permissions = create_group_permissions_table('group_permissions', groups.name, permissions.name, meta)
users = create_users_table('users', meta)
user_groups = create_user_groups_table('user_groups', groups.name, users.name, meta)
sessions = create_sessions_table('sessions', meta)
