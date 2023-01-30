from tabnanny import check
from sqlalchemy import create_engine

import yaml
from ..facebook import facebook_schema
from ..instagram import instagram_schema
from ..twitter import twitter_schema
from ..dboes import dboes_schema
from ..telegram import telegram_schema


class DB_Manager:
    def __init__(self, path=None, config_dict=None):

        if config_dict is not None:
            self.dbuser = config_dict.get("user")
            self.dbpass = config_dict.get("password")
            self.hostname = config_dict.get("localhost")
            self.port = config_dict.get("port")
            self.dbname = config_dict.get("dbname")

        elif path is not None:
            self.path = path
            with open(f"{self.path}/db_config.yaml", "r") as f:
                config = yaml.safe_load(f)

            self.dbuser = config.dbuser
            self.dbpass = config.dbpass
            self.hostname = config.hostame
            self.port = config.port
            self.dbname = config.dbname

        else:
            self.dbuser = "user"
            self.dbpass = "password"
            self.hostname = "localhost"
            self.port = 5432
            self.dbname = "random"

    def create_connection(self):

        engine = create_engine(
            f"postgresql+psycopg2://{self.dbuser}:{self.dbpass}@{self.hostname}:{self.port}/{self.dbname}",
            echo=False
        )

        dboes_schema.metadata.create_all(engine)
        facebook_schema.metadata.create_all(engine)
        instagram_schema.metadata.create_all(engine)
        twitter_schema.metadata.create_all(engine)
        telegram_schema.metadata.create_all(engine)

        return engine
