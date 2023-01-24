"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import logging
from werkzeug.wrappers import Request, Response

from ..helper import helper_instance
from .settings import CONFIG
from m360 import utils

_logger = logging.getLogger(__name__)

class FlaskMiddleware:
    """
    Flask M360 Middleware
    """

    def __init__(self, app, config):
        self.app = app
        self.helper = helper_instance("flask", CONFIG, config)

    def __call__(self, environ, start_response):
        request = Request(environ)
        # handle reserved routes
        data = self.helper.handle_request(request)
        if data:
            if data.get("name"):
                res = Response(utils.to_json(data), status=200, headers={"Content-Type": "application/json"})
                return res(environ, start_response)
            else:
                res = Response(utils.to_json(data), status=500, headers={"Content-Type": "application/json"})
                return res(environ, start_response)

        # continue regular handler execution
        return self.app(environ, start_response)
