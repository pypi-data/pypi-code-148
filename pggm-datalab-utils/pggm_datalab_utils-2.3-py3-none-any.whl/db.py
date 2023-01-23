from contextlib import contextmanager
from datetime import datetime
import json
import logging
import os
import pyodbc
import sqlite3
from typing import Optional, Iterator, Any, Union, Hashable

Record = dict[str, Any]


def get_db_connection(server: str, database: str) -> pyodbc.Connection:
    """
    Initiate pyodbc connection to a SQL Server database. This function is intended to be suitable for cloud development:
    in the cloud you use environment variables to log in under a certain username and password, whereas locally you
    simply log in using your AAD credentials.
    You may specify `DB_DRIVER` to a pyodbc-compatible driver name for your system. It defaults
    to `{ODBC Driver 17 for SQL Server}`. If you specify the value `SQLITE` this routine will use the built-in sqlite3
    library to connect instead.
    By default, this connection will try to log into the database with the user account it's executing under. This is
    compatible with AAD login and suitable for local development. If you want to log into a database from another
    environment, you will have to use Windows credentials. Save the username in the environment variable `DB_UID`,
    the password in `DB_PASSWORD`.
    """
    driver = os.environ.get('DB_DRIVER', '{ODBC Driver 17 for SQL Server}')
    if driver == 'SQLITE':
        logging.info(f'Connecting to SQLite database {database} because driver=SQLITE. Ignoring server {server}.')

        # Make sqlite3 somewhat well-behaved.
        sqlite3.register_converter('datetime', lambda b: datetime.fromisoformat(b.decode()))
        sqlite3.register_converter('json', json.loads)
        sqlite3.register_adapter(list, json.dumps)
        sqlite3.register_adapter(dict, json.dumps)

        return sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
    elif user := os.environ.get('DB_UID', False):
        logging.info(f'Logging into {database}/{server} as {user}.')
        pwd = os.environ['DB_PASSWORD']
        return pyodbc.connect(
            f'Driver={driver};'
            f'Server={server};'
            f'Database={database};'
            f'Uid={os.environ["DB_UID"]};'
            f'Pwd={pwd};')
    else:
        logging.info(f'Logging into {database}/{server} as program user.')
        return pyodbc.connect(
            f'Driver={driver};'
            f'Server={server};'
            f'Database={database};'
            f'trusted_connection=yes;')


@contextmanager
def cursor(db_server: str, db_name: str) -> Iterator[pyodbc.Cursor]:
    """
    Obtain a cursor for a certain database server and database name. Internally uses `get_db_connection`. Use this as
    a context manager, which will handle closing the cursor and the connection. NOTE: this will not handle transaction
    support: most of the time that means you need to commit your transactions yourself!
    Example usage:
    ```
    with cursor('my_server.net', 'test') as c:
        my_data = c.execute('select * from test_database').fetchall()
    ```
    """
    conn = get_db_connection(db_server, db_name)
    c = conn.cursor()
    try:
        yield c
    finally:
        c.close()
        conn.close()


def query(c: pyodbc.Cursor, sql: str, data: Optional[tuple] = None) -> list[dict[str, Any]]:
    """
    Call `c.execute(sql, data).fetchall()` and format the resulting rowset a list of records of the form
    [{colname: value}].

    NOTE: while the type of `c` is a pyodbc Cursor, any DB API 2.0 conforming cursor will work.
    """
    if data is None:
        result = c.execute(sql).fetchall()
    else:
        result = c.execute(sql, data).fetchall()
    headers = [name for name, *_ in c.description]
    return [dict(zip(headers, r)) for r in result]


def get_all(c: pyodbc.Cursor, table_name: str) -> list[dict[str, Any]]:
    """
    Get all current data from table `table_name`.

    IMPORTANT WARNING: `table_name` is not sanitized. Don't pass untrusted table names to this function!
    NOTE: while the type of `c` is a pyodbc Cursor, any DB API 2.0 conforming cursor will work.
    """
    return query(c, f'select * from {table_name}')


def write(c: pyodbc.Cursor, table_name: str, data: list[dict[str, Any]],
          primary_key: Optional[Union[str, tuple]] = None, *, update=True, insert=True, delete=True):
    """
    Update data in database table. We check identity based on the keys of the IndexedPyFrame.
    `update`, `insert`, and `delete` control which actions to take. By default, this function emits the correct update,
    insert, and delete queries to make the database table equal to the in-memory table.
    - `update=True` means rows already in the database will be updated with the in-memory data
    - `insert=True` means rows not already in the database will be added from the in-memory data
    - `delete=True` means rows present in the database but not in the in-memory database will be deleted

    If `primary_key` is None, we will only execute an insert with the in-memory data.

    IMPORTANT WARNING: `table_name` is not sanitized. Don't pass untrusted table names to this function!
    NOTE: while the type of `c` is a pyodbc Cursor, any DB API 2.0 conforming cursor will work.
    """
    # Data checks
    assert len(unique := set(tuple(sorted(r.keys())) for r in data)) == 1, \
        f'Non-uniform list of dictionaries passed, got differing keys {unique}.'
    columns = data[0].keys()

    # Fix up primary key. Either a string or a tuple of length >= 2, and set index.
    if primary_key is None:
        assert not update and not delete, f'Need a primary key to update or delete'
        data = {i: r for i, r in enumerate(data)}
        in_db = set()
    else:
        if isinstance(primary_key, str): primary_key = (primary_key,)
        assert all(isinstance(r[k], Hashable) for r in data for k in primary_key)
        data = {tuple(r[i] for i in primary_key): r for r in data}

        # Modify data so that index columns are in records
        if any(empty_strings := [name for name in columns if any(r[name] == '' for r in data.values())]):
            logging.warning(f'Columns {empty_strings} contain empty strings. '
                            f'Generally inserting empty strings into a database is a bad idea.')

        sql = f'select {", ".join(primary_key)} from {table_name}'
        in_db = {tuple(r[k] for k in primary_key) for r in query(c, sql)}

    if update and (update_keys := data.keys() & in_db):
        update_data = [data[k] for k in update_keys]

        # Use keyword placeholders, so we can pass a record to executemany
        pk_cols = ' AND '.join(f'{col}=:{col}' for col in primary_key)
        assignment = ', '.join(f'{col}=:{col}' for col in columns)
        sql = f'update {table_name} set {assignment} where {pk_cols}'

        c.executemany(sql, update_data)

    if insert and (insert_keys := data.keys() - in_db):
        insert_data = [data[k] for k in insert_keys]

        # Use keyword placeholders, so we can pass a record to executemany
        placeholders = ', '.join(f':{name}' for name in columns)
        columns = ', '.join(columns)
        sql = f'insert into {table_name}({columns}) VALUES ({placeholders})'

        c.executemany(sql, insert_data)

    if delete and (delete_keys := in_db - data.keys()):
        condition = ' AND '.join(f'{k}=?' for k in primary_key)
        sql = f'delete from {table_name} where {condition}'

        c.executemany(sql, list(delete_keys))
