from . import pg2
from .dbtypes import DB_MYSQL
import sqlphile

try:
    import mysql
    from mysql.connector import pooling

except ImportError:
    class open:
        def __init__ (self, *args, **kargs):
            raise ImportError ('mysql-connector-python not installed')
    open3 = open2 = open

else:
    class open (pg2.open):
        dbtype = DB_MYSQL
        def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 3306, dir = None, auto_reload = False, auto_closing = True):
            self.closed = False
            self.auto_closing = auto_closing

            self.conn = None
            host, port = pg2.get_port (host, port)
            self.conn = mysql.connector.connect (user=user, password=password, database = dbname, host = host, port = port)
            self._init (dir, auto_reload, self.dbtype)

    class open2 (pg2.open2):
        dbtype = DB_MYSQL

    class open3 (pg2.open3):
        dbtype = DB_MYSQL

    class open4 (pg2.open4):
        dbtype = DB_MYSQL

    class Pool:
        def __init__ (self, max_conn, dbname, user, password, host = '127.0.0.1', port = 3306, min_conn = 1):
            host, port = pg2.get_port (host, port)
            self.pool = pooling.MySQLConnectionPool (pool_name = "pynative_pool", pool_size = max_conn, pool_reset_session=True, user=user, password=password, host = host, port = port, database = dbname)

        def acquire (self):
            return open4 (self.pool.get_connection (), self.release)

        def release (self, conn):
            conn.close ()

        def close (self):
            pass
