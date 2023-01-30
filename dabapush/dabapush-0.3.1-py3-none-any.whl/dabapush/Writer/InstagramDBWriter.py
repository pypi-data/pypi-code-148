from loguru import logger as log
from .Writer import Writer
from ..Configuration.DBWriterConfiguration import DBWriterConfiguration

smo_database = __import__("smo-database")

class InstagramDBWriter(Writer):
    """
    
    """

    def __init__(self, config):
        super().__init__(config)

        self.initialize_db = smo_database.DB_Manager(
            config_dict={
                "user": config.dbuser,
                "password": config.dbpass,
                "localhost": config.hostname,
                "port": config.port,
                "dbname": config.dbname,
            }
        )

        self.engine = self.initialize_db.create_connection()
        self.instagram_initializer = smo_database.Instagram_Data(self.engine)
        self.instagram_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer

        log.info(f"Persisted {len(data)} records")
        for entry in data:
            self.instagram_initializer.insta_insert(entry)
        self.buffer = []
        # self.instagram_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")
        super().__del__() # this triggers self.persits and must be called

class InstagramDBWriterConfiguration(DBWriterConfiguration):
    """Configuration for the InstagramDBWriter
    """
    yaml_tag = "!dabapush:InstagramDBWriterConfiguration"
    class_instance = InstagramDBWriter

    def get_instance(self) -> InstagramDBWriter:
        return InstagramDBWriter(self)
