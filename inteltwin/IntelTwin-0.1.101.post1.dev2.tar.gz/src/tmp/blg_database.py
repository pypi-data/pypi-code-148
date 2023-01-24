from sshtunnel import SSHTunnelForwarder
import psycopg2
import sqlalchemy
import json


class PsycopgConn:
    _connection: psycopg2 = None

    def __init__(self, conn: psycopg2 = None):
        self._connection = conn

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def __del__(self):
        self._connection.close()

    def test_connection(self, sql_stmt: str):
        result_set = self._connection.cursor()
        result_set.execute(sql_stmt)
        for one_row in result_set:
            print(one_row)


class SqlAlchemyEngine:
    _connection: sqlalchemy.engine = None

    def __init__(self, conn: sqlalchemy.engine = None):
        self._connection = conn

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
#        self._connection.close()

    def __del__(self):
        pass
#        self._connection.close()

    def test_connection(self, sql_stmt):
        result_set = self._connection.execute(sql_stmt)
        for one_row in result_set:
            print(one_row)


class SshTunnel:
    _tunnel_forwarder: SSHTunnelForwarder = None

    def __init__(self, tunnel_forwarder: SSHTunnelForwarder):
        self._tunnel_forwarder = tunnel_forwarder

    def start(self):
        self._tunnel_forwarder.start()

    def get_bind_port(self):
        return self._tunnel_forwarder.local_bind_port

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
#        self._tunnel_forwarder.stop()
#        self._tunnel_forwarder.close()

    def __del__(self):
        pass
#        self._tunnel_forwarder.stop()
#        self._tunnel_forwarder.close()


class BlgDatabase:
    # Declaring Member Variables
    _pg_hostname: str = None
    _pg_username: str = None
    _pg_port: int = None
    _pg_db_name: str = None
    _pg_db_password: str = None
    _ssh_host: str = None
    _ssh_username: str = None
    _ssh_private_key_file: str = None
    _ssh_tunnel: SshTunnel = None
    _psycopg_engine: PsycopgConn = None
    _sqlalchemy_engine: SqlAlchemyEngine = None
    _json_config: {} = None

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
#        del self._sqlalchemy_engine
#        del self._psycopg_engine
#        del self._ssh_tunnel

    def __del__(self):
        pass
#        del self._sqlalchemy_engine
#        del self._psycopg_engine
#        del self._ssh_tunnel

    def __str__(self):
        buf_string = f"PG Hostname:{self._pg_hostname}\n"
        buf_string += f"PG Username:{self._pg_username}\n"
        buf_string += f"PG Port: {self._pg_port}\n"
        buf_string += f"PG Db Name:{self._pg_db_name}\n"
        buf_string += f"PG Db Password:{self._pg_db_password}\n"
        buf_string += f"SSH Host:{self._ssh_host}\n"
        buf_string += f"SSH Username:{self._ssh_username}\n"
        buf_string += f"SSH PKEY File:{self._ssh_private_key_file}\n"
        return buf_string

    def read_json_config(self, json_file_path):
        self._json_config = json.load(open(json_file_path, 'r'))
        self._pg_hostname = self._json_config['PG_HOSTNAME']
        self._pg_username = self._json_config['PG_USERNAME']
        self._pg_port = int(self._json_config['PG_PORT'])
        self._pg_db_name = self._json_config['PG_DB_NAME']
        self._pg_db_password = self._json_config['PG_DB_PW']
        self._ssh_host = self._json_config['SSH_HOST']
        self._ssh_username = self._json_config['SSH_USERNAME']
        self._ssh_private_key_file = self._json_config['SSH_PRIVATE_KEY_FILE']
        return self._json_config

    def set_parameters(self, pg_hostname: str,
                       pg_username: str,
                       pg_port: int,
                       pg_db_name: str,
                       pg_db_password: str,
                       ssh_host: str,
                       ssh_username: str,
                       ssh_private_key_file: str):
        self._pg_hostname = pg_hostname
        self._pg_username = pg_username
        self._pg_port = pg_port
        self._pg_db_name = pg_db_name
        self._pg_db_password = pg_db_password
        self._ssh_host = ssh_host
        self._ssh_username = ssh_host
        self._ssh_private_key_file = ssh_private_key_file

    def init_ssh_tunnel(self):
        remote_bind = (self._pg_hostname, int(self._pg_port))
        if self._ssh_tunnel is None:
            print("Connecting to ssh tunnel....")
            self._ssh_tunnel = SshTunnel(SSHTunnelForwarder(ssh_address_or_host=self._ssh_host,
                                                            ssh_username=self._ssh_username,
                                                            ssh_pkey=self._ssh_private_key_file,
                                                            remote_bind_address=remote_bind))
            self._ssh_tunnel.start()
        return self._ssh_tunnel

    def init_psycopg_engine(self):
        self._psycopg_engine = PsycopgConn(psycopg2.connect(
            user=self._pg_username,
            password=self._pg_db_password,
            database=self._pg_db_name,
            host="localhost",
            port=self._ssh_tunnel.get_bind_port()
        ))
        self._psycopg_engine.test_connection("select * from app_login_subject limit 10;")

        return self._psycopg_engine

    def init_sqlalchemy_engine(self):
        self._sqlalchemy_engine = SqlAlchemyEngine(
            sqlalchemy.create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
                host="localhost",
                port=self._ssh_tunnel.get_bind_port(),
                user=self._pg_username,
                password=self._pg_db_password,
                db=self._pg_db_name)))
        self._sqlalchemy_engine.test_connection("select * from app_login_subject limit 10;")
        return self._sqlalchemy_engine
