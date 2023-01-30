from . import pg2
from .dbtypes import DB_ORACLE
import sqlphile

try:
    import cx_Oracle

except ImportError:
    class open:
        def __init__ (self, *args, **kargs):
            raise ImportError ('cx_Oracle not installed')
    open3 = open2 = open

else:
    class open (pg2.open):
        dbtype = DB_ORACLE
        def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 1521, dir = None, auto_reload = False, auto_closing = True):
            self.closed = False
            self.auto_closing = auto_closing

            self.conn = None
            host, port = pg2.get_port (host, port)
            self.conn = cx_Oracle.connect (user=user, password=password, dsn = f'{host}:{port}/{dbname}')
            self._init (dir, auto_reload, self.dbtype)

    class open2 (pg2.open2):
        dbtype = DB_ORACLE

    class open3 (pg2.open3):
        dbtype = DB_ORACLE

    class open4 (pg2.open4):
        dbtype = DB_ORACLE

    class Pool:
        def __init__ (self, max_conn, dbname, user, password, host = '127.0.0.1', port = 1521, min_conn = 1):
            host, port = pg2.get_port (host, port)
            self.pool = cx_Oracle.SessionPool (min = min_conn, max = max_conn, increment = 1, user=user, password=password, dsn = f'{host}:{port}/{dbname}')

        def acquire (self):
            return open4 (self.pool.acquire (), self.release)

        def release (self, conn):
            self.pool.release (conn)

        def close (self):
            self.pool.close ()

