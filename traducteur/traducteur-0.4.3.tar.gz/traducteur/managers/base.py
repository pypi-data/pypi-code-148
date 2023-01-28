class BaseModelManager:
    def __init__(self, connection_string: str, database_name):
        self.connection_string = connection_string
        self.database_name = database_name
        