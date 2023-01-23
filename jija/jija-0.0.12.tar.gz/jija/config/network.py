from jija.config import base, fields


class NetworkConfig(base.Config):
    HOST = fields.CharField(default='0.0.0.0')
    PORT = fields.IntegerField(default=8080)

    def __init__(self, *, host=None, port=None):
        super().__init__(host=host, port=port)
