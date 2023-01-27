import psycopg2
from psycopg2.extras import RealDictCursor

pg_conn_str: str = ''


def configure(host: str, port: int, dbname: str, usrid: str, pwd: str) -> None:
    """
    Configure postgresql connection string
    :param host: host
    :param port: port
    :param dbname: dbname
    :param usrid: usrid
    :param pwd: password
    :return: None
    """
    global pg_conn_str
    pg_conn_str = f"host='{host}' port={port} dbname='{dbname}' user={usrid} password={pwd}"


def get(q: str):
    """
    Execute query
    :param q: query
    :return: Result list
    """
    global pg_conn_str
    with psycopg2.connect(pg_conn_str) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(q)
            rs = cur.fetchall()
        return rs


def set(stmt: str) -> None:
    """
    Execute statement
    :param stmt: statement
    :return: None
    """
    global pg_conn_str
    with psycopg2.connect(pg_conn_str) as conn:
        with conn.cursor() as cur:
            cur.execute(stmt)
