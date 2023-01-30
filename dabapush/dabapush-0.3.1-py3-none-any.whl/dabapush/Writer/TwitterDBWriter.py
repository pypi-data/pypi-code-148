from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

smo_database = __import__("smo-database")


class TwitterDBWriter(Writer):
    """ """

    def __init__(self, config: "TwitterDBWriterConfiguration"):
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
        self.twitter_initializer = smo_database.Twitter_Data(self.engine)
        self.twitter_initializer.create_local_session()

    def persist(self):
        """

        Parameters
        ----------
        Returns
        -------

        """
        data = self.buffer
        self.buffer = []

        for _ in data:
            self.twitter_initializer.twitter_insert(_)
            
        self.twitter_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")
        super().__del__()

class TwitterDBWriterConfiguration(DBWriterConfiguration):
    yaml_tag = "!dabapush:TwitterDBWriterConfiguration"

    def get_instance(self):
        """ """
        return TwitterDBWriter(self)
