import pandas as pd
import sqlalchemy

_db_engine = ''
_db_connection = ''


def db_connect(url):
    """Connect and save connection to a PostgreSQL database."""
    global _db_engine, _db_connection

    _db_engine = sqlalchemy.create_engine(url)
    _db_connection = _db_engine.connect()
    print('Connected to database.')


def db_execute(sql, read=True):
    """Execute the given SQL. If read_mode = True, then returns a pandas dataframe containing the response."""

    global _db_engine, _db_connection

    if read: return pd.read_sql_query(sql, _db_engine)
    else: _db_connection.execute(sql + '\ncommit;')

