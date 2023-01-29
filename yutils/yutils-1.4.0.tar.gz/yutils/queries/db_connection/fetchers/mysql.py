#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.queries.db_connection.fetchers.base_fetcher import BaseFetcher

create_engine = None
sessionmaker = None
def _import():
    global create_engine
    global sessionmaker
    if create_engine is None:
        from sqlalchemy import create_engine
    if sessionmaker is None:
        from sqlalchemy.orm.session import sessionmaker


class MySQLFetcher(BaseFetcher):
    _CONNECTION_STRING = "mysql+pymysql://{username}:{password}@{host}/{schema}?charset={encoding}"
    _ENCODING = "utf8mb4"

    def __init__(self, connection_details, verbose=True):
        _import()
        super().__init__(connection_details, verbose)

        self.engine = None
        self.session = None
        self.connect()

    def execute(self, query):
        execution = self.session.execute(query)
        if not execution.returns_rows or not execution.keys():
            return  # this may happen when queries are DML/DDL, so they have no return value.
        fields = execution.keys()
        results = execution.fetchall()
        results = [list(row) for row in results]
        return self._organize_results(results, fields)

    def connect(self):
        connection_string = self._CONNECTION_STRING.format(username=self.connection_details.USERNAME,
                                                           password=self.connection_details.PASSWORD,
                                                           host=self.connection_details.HOST,
                                                           schema=self.connection_details.SCHEMA,
                                                           encoding=self._ENCODING)
        self.engine = create_engine(connection_string)
        self.engine.connect()
        self.session = sessionmaker()(bind=self.engine, autoflush=False, expire_on_commit=True)
        self.engine.echo = False
        self.engine.encoding = 'utf8'

    def disconnect(self):
        if self.session:
            self.session.expire_all()
            self.session.expunge_all()
            self.session.close_all()
            for key in self.session.identity_map.keys():
                self.session.identity_map.remove_key(key)
            self.session.connection().close()
            self.session.close()
            self.engine.dispose()

    def commit(self):
        self.session.commit()
