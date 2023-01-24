"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import json
import logging

from m360 import utils
from m360.gateway import connector

_logger = logging.getLogger(__name__)
_connector = connector.instance()

class User(object):
    """Offers user related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("User created")

    @staticmethod
    def user_singleton():
        """Access the singleton receiver"""

        if User._instance:
            return User._instance

        if not User._instance:
            _logger.debug("Creating user instance")
            User._instance = User()

        return User._instance

    @staticmethod
    def get(request):
        if not request:
            return None
        headers = utils.get_req_headers(request)
        if not headers or not headers.get("m360"):
            return None
        try:
            m360 = headers.get("m360")
            if m360:
                m360 = json.loads(m360)
        except Exception as e:
            _logger.error(e)
            m360 = None

        return m360.get("user") if m360 and type(m360) is dict and m360.get("user") else None

    @staticmethod
    def find(context):
        user_id = str(context.get("id")) if context.get("id") else None
        start = context.get("start") if context.get("start") else 1
        limit = context.get("limit") if context.get("limit") else 100
        group = context.get("group")
        service = context.get("service")
        version = context.get("version")
        tenant = context.get("tenant")
        url = "/users/" + user_id if user_id else "/users"
        qs = {}

        if not user_id:
            qs["start"] = start
            qs["limit"] = limit
        if group:
            qs["group"] = group
        if tenant:
            qs["tenant"] = tenant
        if service:
            qs["service"] = service
        if version:
            qs["version"] = version

        return _connector.invoke({"route": url, "qs": qs})

def instance():
    """Get the singleton instance of the user"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return User.user_singleton()
