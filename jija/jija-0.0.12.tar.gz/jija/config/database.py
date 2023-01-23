from jija.config import base, fields


class DatabaseConfig(base.Config):
    DATABASE = fields.CharField()
    PASSWORD = fields.CharField()
    USER = fields.CharField(default='postgres')
    PORT = fields.IntegerField(default=5432)
    HOST = fields.CharField(default='localhost')

    def __init__(self, *, database, password, host=None, user=None, port=None):
        super().__init__(database=database, password=password, host=host, user=user, port=port)

    @classmethod
    async def preflight(cls):
        from jija import config
        await config.DriversConfig.DATABASE.preflight()
