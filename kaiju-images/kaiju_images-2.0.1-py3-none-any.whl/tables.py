import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

from kaiju_files.tables import files


def create_images_table(table_name: str, file_table, metadata: sa.MetaData, *columns: sa.Column):
    """
    :param table_name: custom table name
    :param file_table: files table definition
    :param metadata: custom metadata object
    :param columns: additional columns
    """

    return sa.Table(
        table_name, metadata,
        sa.Column(
            'id', sa_pg.UUID, nullable=False, primary_key=True,
            server_default=sa.text("uuid_generate_v4()")),
        sa.Column('version', sa_pg.VARCHAR, nullable=True),
        sa.Column(
            'correlation_id', sa_pg.UUID, nullable=False,
            server_default=sa.text("uuid_generate_v4()")),
        sa.Column(
            'timestamp', sa_pg.TIMESTAMP, nullable=False,
            server_default=sa.func.timezone('UTC', sa.func.current_timestamp())
        ),
        sa.Column(
            'original_id', None,
            sa.ForeignKey(f'{table_name}.id', onupdate="RESTRICT", ondelete="CASCADE"),
            nullable=True
        ),
        sa.Column(
            'file_id', None,
            sa.ForeignKey(file_table.c.id, onupdate="RESTRICT", ondelete="CASCADE"),
            nullable=True
        ),
        sa.Column(
            'meta', sa_pg.JSONB, nullable=False,
            server_default=sa.text("'{}'::jsonb")
        ),
        sa.Index(
            'idx_photo_version', 'version',
            postgresql_using='hash',
        ),
        sa.Index(
            'idx_photo_correlation_id', 'correlation_id',
            postgresql_using='hash',
        ),
        sa.Index(
            'idx_photo_timestamp', 'timestamp',
            postgresql_using='btree', postgresql_ops={'timestamp': 'DESC'}
        ),
        *columns
    )


images = create_images_table('images', files, sa.MetaData())


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
