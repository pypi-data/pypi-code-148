from jija.config import base, fields

from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_session


class AuthConfig(base.Config):
    SECRET_KEY: str = fields.CharField()

    def __init__(self, *, secret_key):
        super().__init__(secret_key=secret_key)

    @classmethod
    def base_app_update(cls, aiohttp_app):
        aiohttp_session.setup(aiohttp_app, EncryptedCookieStorage(cls.SECRET_KEY))
        return aiohttp_app
