from typing import Optional
from pymongo import MongoClient
from . import BaseDatabaseContext


class MongoContext(BaseDatabaseContext):
    def __init__(self, connection_string: str, db_name: str, column_name: Optional[str] = None):
        super().__init__(connection_string, db_name)
        
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]
        self.col = column_name

    def __enter__(self):
        return self.db[self.col] if self.col else self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        