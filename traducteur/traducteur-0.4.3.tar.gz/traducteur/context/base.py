class BaseDatabaseContext(object):
    def __init__(self, connection_string: str, db_name: str):
        self.connection_string = connection_string
        self.db_name = db_name

    def __exit__(self, exc_type, exc_value, traceback):
        pass
    