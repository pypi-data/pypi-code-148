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

class Tenant(object):
    """Offers tenant related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Tenant created")

    @staticmethod
    def tenant_singleton():
        """Access the singleton receiver"""

        if Tenant._instance:
            return Tenant._instance

        if not Tenant._instance:
            _logger.debug("Creating tenant instance")
            Tenant._instance = Tenant()

        return Tenant._instance

    @staticmethod
    def get(request, code):
        if not code or not code.strip() or not request:
            return None
        headers = utils.get_req_headers(request)
        if not headers or "m360" not in headers:
            return None

        try:
            m360 = headers.get("m360")
            if m360:
                m360 = json.loads(m360)
        except Exception as e:
            _logger.error(e)
            m360 = None

        if not m360 or "tenants" not in m360 or type(m360.get("tenants")) is not list:
            _logger.error("Invalid schema for m360=" + str(m360))
            return None

        tenant = None
        for t in m360.get("tenants"):
            if t and t.get("code") == code:
                tenant = t
                break
        return tenant

    @staticmethod
    def list(request):
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

        if not m360 or not m360.get("tenants") or type(m360.get("tenants")) is not list:
            _logger.error("Invalid schema for m360=" + str(m360))
            return None

        return m360.get("tenants")

    @staticmethod
    def find(codes=None):
        code = codes if codes else []
        url = "/tenants"
        body = {"code": code}

        return _connector.invoke({"route": url, "method": "post", "body": body})

def instance():
    """Get the singleton instance of the tenant"""
    _logger.debug("calling tenant_instance, os.pid=%d", os.getpid())
    return Tenant.tenant_singleton()
