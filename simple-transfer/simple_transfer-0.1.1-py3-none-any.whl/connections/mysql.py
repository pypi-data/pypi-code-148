import io
import logging
import os
from typing import Generator, Iterable, Optional, Sequence, TextIO, Tuple, Union
from uuid import uuid4

import mysql.connector
import mysql.connector.connection
import mysql.connector.cursor
import mysql.connector.pooling
from simple_transfer.column import Column
from simple_transfer.config import SIMPLE_TRANSFER_CONFIG
from simple_transfer.connection import Connection, NotConnectedException

TABLE_COLUMNS_QUERY = """
select column_name as "column"
    , is_nullable as is_nullable
    , data_type as data_type
    , character_maximum_length as varchar_length
from information_schema.columns c
where c.table_schema = %s
    and c.table_name = %s
order by c.ordinal_position asc;
""".strip()

BASE_CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS {schema}.{table} (
{columns}
);
""".strip()

BASE_SELECT_STAR_TABLE_QUERY = """
SELECT *
FROM {schema}.{table}{where};
""".strip()

BASE_DROP_TABLE_QUERY = """
DROP TABLE IF EXISTS {schema}.{table};
""".strip()

BASE_RENAME_TABLE_QUERY = """
RENAME TABLE {schema}.{table}
TO {new_table};
""".strip()


class MySQLConnection(Connection):
    """
    The interface with which the simple-transfer package interacts with a MySQL database.
    This class implements the `Connection` interface.
    """

    conn: Union[
        None,
        mysql.connector.connection.MySQLConnection,
        mysql.connector.pooling.PooledMySQLConnection,
    ]

    def __init__(
        self, host: str, port: int, username: str, password: str, db: str = "postgres"
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.conn = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.db,
            use_pure=False,
            allow_local_infile=True,
        )
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Connected to MySQL server `{self.host}:{self.port}`")

    def close(self):
        if self.conn == None:
            return
        if not self.conn.is_connected():
            return
        self.conn.close()
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Disconnected from MySQL server `{self.host}:{self.port}`")
        return

    @staticmethod
    def _cursor_fetch_generator(
        cursor: mysql.connector.cursor.MySQLCursor,
        batch_size: int = SIMPLE_TRANSFER_CONFIG.BATCH_SIZE,
    ):
        index = 0
        while True:
            batch = cursor.fetchmany(batch_size)
            if len(batch) == 0:
                break
            for record in batch:
                yield record
                index += 1
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(f"Returned {index} rows")
        cursor.close()

    def select(
        self,
        query: str,
        args: Optional[Sequence] = None,
        batch_size: int = SIMPLE_TRANSFER_CONFIG.BATCH_SIZE,
    ) -> Generator[Tuple, None, None]:
        if self.conn is None:
            raise NotConnectedException()
        cursor = self.conn.cursor()
        if SIMPLE_TRANSFER_CONFIG.VERBOSE:
            logging.info(f"Executing query:\n{query}")
        cursor.execute(query, params=args)
        return self._cursor_fetch_generator(cursor, batch_size=batch_size)

    def execute(self, query: str, args: Optional[Sequence] = None):
        if args is None:
            args = []
        if self.conn is None:
            raise NotConnectedException()
        with self.conn.cursor() as cursor:
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(f"Executing query:\n{query}")
            cursor.execute(query, params=args)
            self.conn.commit()

    def execute_many(self, queries: Iterable[str], args: Iterable[Sequence] = []):
        if self.conn is None:
            raise NotConnectedException()
        with self.conn.cursor() as cursor:
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info("Starting transaction")
            for query, q_args in zip(queries, args):
                if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                    logging.info(f"Executing query:\n{query}")
                cursor.execute(query, params=q_args)
            self.conn.commit()
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info("Ending transaction")

    def extract_table_ddl(self, schema: str, table: str) -> Iterable[Column]:
        if self.conn is None:
            raise NotConnectedException()

        raw_columns = self.select(
            TABLE_COLUMNS_QUERY,
            args=[
                schema,
                table,
            ],
        )
        columns = []
        for raw_column in raw_columns:
            raw_column = [
                col.decode() if isinstance(col, bytes) else col for col in raw_column
            ]
            columns.append(
                Column(
                    name=raw_column[0],
                    data_type=raw_column[2],
                    is_nullable=raw_column[1] == "YES",
                    varchar_length=raw_column[3],  # type: ignore
                )
            )

        return columns

    def extract_table(
        self, schema: str, table: str, where_clause: str = ""
    ) -> Generator[Tuple, None, None]:
        if self.conn is None:
            raise NotConnectedException()
        f_where = "" if where_clause == "" else f"\nWHERE {where_clause}"
        return self.select(
            BASE_SELECT_STAR_TABLE_QUERY.format(
                schema=schema, table=table, where=f_where
            ),
            batch_size=SIMPLE_TRANSFER_CONFIG.BATCH_SIZE,
        )

    def import_csv(self, schema: str, table: str, f: TextIO):
        remote_file = False
        if self.conn is None:
            raise NotConnectedException()
        try:
            f.fileno()
            csv_abs_path = os.path.abspath(f.name)
        except io.UnsupportedOperation:
            remote_file = True
            if SIMPLE_TRANSFER_CONFIG.VERBOSE:
                logging.info(f"File is remote, must download before uploading to MySQL")
            temp_file_name = f"temp_mysql_{uuid4().hex}.csv"
            with open(temp_file_name, "w") as temp_file:
                for line in f:
                    temp_file.write(line)
            csv_abs_path = os.path.abspath(temp_file_name)
        self.execute(
            f"LOAD DATA LOCAL INFILE '{csv_abs_path}' INTO TABLE {schema}.{table} FIELDS TERMINATED BY ',' IGNORE 1 ROWS;"
        )
        if remote_file:
            os.remove(csv_abs_path)

    @staticmethod
    def _generate_column_statement(
        column: Column,
    ):
        extra_datatype = f"({column.varchar_length})" if column.varchar_length else ""
        return f'{column.name} {column.data_type}{extra_datatype} {"" if column.is_nullable else "NOT NULL"}'

    @staticmethod
    def generate_create_table_statement(
        schema: str,
        table: str,
        columns: Iterable[Column],
    ) -> str:
        return BASE_CREATE_TABLE_QUERY.format(
            schema=schema,
            table=table,
            columns="\n    ,".join(
                [
                    MySQLConnection._generate_column_statement(column)
                    for column in columns
                ]
            ),
        )

    @staticmethod
    def generate_drop_table_statement(schema: str, table: str) -> str:
        return BASE_DROP_TABLE_QUERY.format(
            schema=schema,
            table=table,
        )

    @staticmethod
    def generate_rename_table_statement(schema: str, table: str, new_table: str) -> str:
        return BASE_RENAME_TABLE_QUERY.format(
            schema=schema, table=table, new_table=new_table
        )

    def __str__(self):
        return f"MySQL DB `{self.host}:{self.port}` `{self.db}`"
