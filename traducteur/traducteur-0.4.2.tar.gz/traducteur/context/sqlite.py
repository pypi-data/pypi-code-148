import sqlite3

from .base import BaseDatabaseContext


class SQLite3Context(BaseDatabaseContext):
    def __init__(self, connection_string: str, db_name: str = ''):
        super().__init__(connection_string, db_name)

        self.client = sqlite3.connect(self.connection_string)
        
    def __enter__(self):
        return self.client.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        super().__exit__(exc_type, exc_value, traceback)
        self.client.commit()
        self.client.close()
