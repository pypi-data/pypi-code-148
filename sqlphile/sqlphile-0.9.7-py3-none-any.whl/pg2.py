from . import db3
from .dbtypes import DB_PGSQL, DB_SQLITE3
import sqlphile

def get_port (host, port):
    if ":" in host:
        host, port = host.split (":")
        port = int (port)
    return host, port


try:
    import psycopg2

except ImportError:
    class open:
        def __init__ (self, *args, **kargs):
            raise ImportError ('psycopg2 not installed')
    open3 = open2 = open

else:
    from psycopg2.pool import ThreadedConnectionPool

    class open (db3.open):
        dbtype = DB_PGSQL
        def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 5432, dir = None, auto_reload = False, auto_closing = True):
            self.closed = False
            self.auto_closing = auto_closing

            self.conn = None
            host, port = get_port (host, port)
            self.conn = psycopg2.connect (host=host, dbname=dbname, user=user, password=password, port = port)
            self._init (dir, auto_reload, self.dbtype)

        def field_names (self):
            return [x.name for x in self.description]

        def set_autocommit (self, flag = True):
            self.conn.autocommit = flag


    class open2 (open, db3.open2):
        dbtype = DB_PGSQL
        def __init__ (self, conn, dir = None, auto_reload = False, auto_closing = True):
            db3.open2.__init__ (self, conn, dir, auto_reload, auto_closing)


    class open3 (open2, db3.open3):
        dbtype = DB_PGSQL
        def __init__ (self, conn, dir = None, auto_reload = False):
            db3.open3.__init__ (self, conn, dir, auto_reload)

    class open4 (open2, db3.open4):
        dbtype = DB_PGSQL
        def __init__ (self, conn, pool, dir = None, auto_reload = False):
            db3.open4.__init__ (self, conn, pool, dir, auto_reload)

    class Pool:
        def __init__ (self, max_conn, dbname, user, password, host = '127.0.0.1', port = 5432, min_conn = 1):
            host, port = get_port (host, port)
            self.pool = ThreadedConnectionPool (min_conn, max_conn, host = host, dbname = dbname, user = user, password = password, port = port)

        def acquire (self):
            return open4 (self.pool.getconn (), self.release)

        def release (self, conn):
            self.pool.putconn (conn)

        def close (self):
            self.pool.closeall ()
