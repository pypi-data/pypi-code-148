import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

__all__ = [
    'create_file_table', 'files', 'create_converters_table', 'converters'
]


def create_file_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """
    :param table_name: custom table name
    :param metadata: custom metadata object
    :param columns: additional columns
    """

    return sa.Table(
        table_name, metadata,
        sa.Column('id', sa_pg.UUID, primary_key=True, server_default=sa.text("uuid_generate_v4()")),
        sa.Column('hash', sa_pg.UUID, nullable=True),
        sa.Column('name', sa_pg.VARCHAR, nullable=True),
        sa.Column('extension', sa_pg.VARCHAR, nullable=True),
        sa.Column(
            'timestamp', sa_pg.TIMESTAMP, nullable=False,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp())
        ),
        sa.Column(
            'meta', sa_pg.JSONB, nullable=False,
            server_default=sa.text("'{}'::jsonb")
        ),
        sa.Index(f'idx_{table_name}_hash', 'hash', postgresql_using='hash'),
        sa.Index(f'idx_{table_name}_ext', 'extension', postgresql_using='hash'),
        sa.Index(f'idx_{table_name}_name', 'name', postgresql_using='hash'),
        sa.Index(
            f'idx_{table_name}_timestamp', 'timestamp',
            postgresql_using='btree', postgresql_ops={'timestamp': 'DESC'}
        ),
        *columns
    )


files = create_file_table('file', sa.MetaData())


def create_converters_table(table_name: str, metadata: sa.MetaData, *columns: sa.Column):
    """
    :param table_name: custom table name
    :param metadata: custom metadata object
    :param columns: additional columns
    """

    return sa.Table(
        table_name, metadata,
        sa.Column(
            'id', sa_pg.UUID, nullable=False, primary_key=True,
            server_default=sa.text("uuid_generate_v4()")),
        sa.Column('cls', sa_pg.VARCHAR, nullable=False),
        sa.Column('name', sa_pg.TEXT, nullable=False, unique=True),
        sa.Column('system', sa_pg.BOOLEAN, nullable=False, default=False),
        sa.Column('settings', sa_pg.JSONB, nullable=False),
        sa.Column(
            'timestamp', sa_pg.TIMESTAMP, nullable=False,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp())
        ),
        *columns
    )


converters = create_converters_table('converters', sa.MetaData())
