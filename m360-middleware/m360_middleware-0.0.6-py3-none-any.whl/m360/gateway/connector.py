"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import re
import logging

from m360 import constants, utils

_logger = logging.getLogger(__name__)
_ip_pattern = re.compile("^([0-9]{1,3}\\.){3}[0-9]{1,3}$")

class Connector(object):
    """Handles communication with the gateway"""

    # singleton
    _instance = None

    _service_name = None
    _service_version = None

    def __init__(self):
        _logger.debug("Connector created")

    def init(self, service_name, service_version):
        self._service_name = service_name
        self._service_version = service_version
        _logger.debug("Connector init complete")

    @staticmethod
    def connector_singleton():
        """Access the singleton receiver"""

        if Connector._instance:
            return Connector._instance

        if not Connector._instance:
            _logger.debug("Creating connector instance")
            Connector._instance = Connector()

        return Connector._instance

    def invoke(self, context=None):
        """Invokes gateway APIs"""
        _logger.debug("Invoking connector with the context: " + str(context))

        if not context:
            context = {}
        ip = str(context.get("ip")) if context.get("ip") else constants.GATEWAY_MAINTENANCE_IP
        ip = ip.replace("https://", "").replace("http://", "").replace("/", "")
        port = context.get("port") if context.get("port") else constants.GATEWAY_MAINTENANCE_PORT
        http_method = context.get("method").lower() if context.get("method") else "get"
        route = context.get("route") if context.get("route") else ""

        # build uri
        if ip != "localhost" and not _ip_pattern.match(ip):
            url = "https://" + ip + route
        else:
            url = "https://" + ip + ":" + str(port) + route

        # build headers
        headers = context.get("headers") if context.get("headers") else {}
        if self._service_name:
            headers["service"] = self._service_name
        if self._service_version:
            headers["version"] = str(self._service_version)

        query = context.get("qs") if context.get("qs") else None
        body = context.get("body") if context.get("body") else None

        max_count = int(context.get("retryOnFailure")) if context.get("retryOnFailure") else 1
        delay = int(context.get("retryDelay")) if context.get("retryDelay") else 5

        # make request with retry strategy
        res = utils.retry_request(url=url, method=http_method, headers=headers, query=query, body=body, is_json=True,
                                  retries=(max_count - 1), retry_delay=delay).json()
        if "result" in res and "data" in res:
            return res.get("data")
        else:
            return res

def instance():
    """Get the singleton instance of the connector"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return Connector.connector_singleton()
