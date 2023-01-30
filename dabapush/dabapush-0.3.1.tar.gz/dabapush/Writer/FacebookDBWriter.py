from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

# from ...smo_database import DB_Manager, Facebook_Data
smo_database = __import__("smo-database")


class FacebookDBWriter(Writer):
    """ """

    def __init__(self, config):

        self.initialize_db = smo_database.DB_Manager(config)
        self.engine = self.initialize_db.create_connection()
        self.facebook_initializer = smo_database.Facebook_Data(self.engine)
        self.facebook_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        self.facebook_initializer.fb_insert(data)

    def __del__(self):
        print("Session and Connection Terminated")


class FacebookDBWriterConfiguration(DBWriterConfiguration):
    yaml_tag = "!dabapush:FacebookDBWriterConfiguration"

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        user: str = "postgres",
        password: str = "password",
        dbname: str = "public",
        host: str = "localhost",
        port: int = 5432,
    ) -> None:
        super().__init__(name, id, chunk_size, user, password, dbname, host, port)

    def get_instance(self):
        """ """
        return FacebookDBWriter(self)
