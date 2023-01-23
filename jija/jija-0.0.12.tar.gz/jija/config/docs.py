from os.path import abspath

from aiohttp import web
from jija import docs
from . import base, fields
import os


class DocsConfig(base.Config):
    URL: str = fields.CharField(default='/docs')

    def __init__(self, url=None):
        super().__init__(url=url)

    @classmethod
    def base_app_update(cls, aiohttp_app):
        docs_setuper = docs.DocsSetup(aiohttp_app)
        aiohttp_app = docs_setuper.setup()
        return aiohttp_app


async def ping(request):
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
    """
    return web.Response(text="pong")