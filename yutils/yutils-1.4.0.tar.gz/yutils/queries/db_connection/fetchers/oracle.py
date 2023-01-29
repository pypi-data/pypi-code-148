#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils.queries.db_connection.fetchers.base_fetcher import BaseFetcher


cx = None
def _import():
    global cx
    if cx is None:
        import cx_Oracle as cx


class OracleFetcher(BaseFetcher):
    _LOB_TYPES = []
    _FIELD_TYPES_NOT_TO_DECODE = []

    def __init__(self, connection_details, verbose=True):
        _import()
        self._write_constants()
        super().__init__(connection_details, verbose)

        self.connection = None
        self.connect()
        self.cursor = self.connection.cursor()

    def _write_constants(self):
        self._LOB_TYPES = [cx.LOB, cx.BLOB, cx.CLOB]
        self._FIELD_TYPES_NOT_TO_DECODE = self._LOB_TYPES + [cx.BINARY]

    def execute(self, query):
        execution = self.cursor.execute(query)

        if execution is None:  # this may happen when queries are DML/DDL, so they have no return value.
            return

        fields = [field[0].lower().decode(self._EXPECTED_ENCODING) for field in execution.description]
        field_types = {field[0].lower().decode(self._EXPECTED_ENCODING): field[1] for field in execution.description}

        results = []
        for row in execution:
            row = list(row)
            results.append(self._read_lobs(row, fields, field_types))
        return self._organize_results(results, fields, field_types)

    def _read_lobs(self, row, fields, field_types):
        for i in range(len(row)):
            if field_types[fields[i]] in self._LOB_TYPES:
                if row[i]:
                    row[i] = row[i].read()
        return row

    def connect(self):
        self.connection = cx.connect(self.connection_details.SCHEMA,
                                     self.connection_details.PASSWORD,
                                     self.connection_details.DB)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()
