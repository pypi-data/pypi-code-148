from ..Configuration.DBWriterConfiguration import DBWriterConfiguration
from .Writer import Writer

smo_database = __import__("smo-database")


class TelegramDBWriter(Writer):
    """ """

    def __init__(self, config: "TelegramDBWriterConfiguration"):
        super().__init__(config)

        self.db = smo_database.DB_Manager(
            config_dict={
                "user": config.dbuser,
                "password": config.dbpass,
                "localhost": config.hostname,
                "port": config.port,
                "dbname": config.dbname,
            }
        )
        self.engine = self.db.create_connection()
        self.telegram_initializer = smo_database.Telegram_Data(self.engine)
        self.telegram_initializer.create_local_session()

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
            self.telegram_initializer.telegram_insert(_)

        self.telegram_initializer.local_session.commit()

    def __del__(self):
        print("Session and Connection Terminated")
        super().__del__()


class TelegramDBWriterConfiguration(DBWriterConfiguration):
    yaml_tag = "!dabapush:TelegramDBWriterConfiguration"

    def get_instance(self):
        """ """
        return TelegramDBWriter(self)
