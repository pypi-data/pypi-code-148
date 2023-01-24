"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import logging

from m360 import user, constants, utils
from m360.gateway import connector
from m360.ttlcache import TTLCache

_logger = logging.getLogger(__name__)
_connector = connector.instance()

def get_config(config, microservice):
    final_config = {}
    if config:
        # check and merge common config
        if config.get("common"):
            for key, val in config.get("common"):
                final_config[key] = val
        # check and merge specific microservice config
        if config.get("specific") and microservice and config.get("specific").get(microservice):
            temp_config = config.get("specific").get(microservice).get("config")
            if not temp_config:
                temp_config = config.get("specific").get(microservice)
            for key, val in temp_config:
                final_config[key] = val
            if config.get("specific").get(microservice).get("config") \
                    and config.get("specific").get(microservice).get("version"):
                final_config["__M360SV_" + microservice] = config.get("specific").get(microservice).get("version")
    # return merged config
    return final_config

class Awareness(object):
    """Offers awareness related helper methods"""

    # singleton
    _instance = None

    _ttl = 30
    _cache = TTLCache(ttl=_ttl)

    def __init__(self):
        _logger.debug("Awareness created")

    def init(self, ttl=None):
        if not ttl:
            ttl = constants.DEFAULT_AWARENESS_TTL_MS
        self._ttl = ttl / 1000
        _logger.debug("Awareness init complete")

    @staticmethod
    def awareness_singleton():
        """Access the singleton receiver"""

        if Awareness._instance:
            return Awareness._instance

        if not Awareness._instance:
            _logger.debug("Creating awareness instance")
            Awareness._instance = Awareness()

        return Awareness._instance

    def reload(self, ip=None, port=None, headers=None):
        self._cache.clear()
        return self.get(ip, port, headers)

    def get(self, ip=None, port=None, headers=None):
        no_cache = True if headers and headers.get("Cache-Control") == "no-cache" else False
        cache_key = str(ip) + "_" + str(port)
        cached = self._cache.get(cache_key)

        # return cached version if found
        if not no_cache and cached:
            return cached

        res = _connector.invoke({"ip": ip, "port": port, "headers": headers, "route": "/awareness"})
        # cache the value for next time
        self._cache.set(cache_key, res, self._ttl)
        return res

    @staticmethod
    def get_next_host(service, version, ip=None, port=None):
        qs = {"service": service, "version": version}
        return _connector.invoke({"ip": ip, "port": port, "route": "/service/nextHost", "qs": qs})

    @staticmethod
    def proxy(context):
        host = Awareness.get_next_host(context.get("service"), context.get("version"), context.get("gatewayIp"),
                                       context.get("gatewayPort"))

        if context.get("user"):
            user_doc = user.instance().find({"id": context.get("user")})

            if not user_doc:
                raise Exception("User Not Found!")

            if not context.get("headers"):
                context["headers"] = {}
            context["headers"]["m360"] = user_doc.get("m360")

            if user_doc.get("tenants"):
                context["headers"]["m360"]["tenants"] = []
                for t in user_doc.get("tenants"):
                    tenant = {
                        "id": t.get("id"),
                        "code": t.get("code"),
                        "config": get_config(user_doc.get("config").get(t.get("code")), context.get("service"))
                    }
                    context["headers"]["m360"]["tenants"].append(tenant)

            context["headers"]["m360"] = utils.to_json(context["headers"]["m360"])

        return _connector.invoke({"ip": host.get("ip"), "port": host.get("port"), "route": context.get("route"),
                                  "qs": context.get("qs"), "body": context.get("body"), "method": context.get("method"),
                                  "headers": context.get("headers")})

def instance():
    """Get the singleton instance of the awareness"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return Awareness.awareness_singleton()
