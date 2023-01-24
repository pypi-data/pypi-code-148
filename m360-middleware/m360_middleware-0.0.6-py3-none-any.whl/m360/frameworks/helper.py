"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import logging
import threading

from m360 import sdk, constants
from m360.maintenance import Maintenance

_logger = logging.getLogger(__name__)

class Helper:
    """
    M360 Middleware Helper
    """

    # singleton
    _instance = None

    def __init__(self, framework, default_config, config=None):
        _logger.info("M360 middleware config: " + str(config))
        self.framework = framework
        self.config = self.init_config(default_config, config)
        _logger.info("M360 middleware merged config: " + str(self.config))

        # M360 SDK initialization
        self.sdk = sdk.instance()
        self.sdk.init(self.config)
        self.sdk.augment(self.config)
        self.app_name = self.config.get("contract", {}).get("name", "noname")
        self.maintenance = Maintenance(self.config, self.app_name, self.sdk.registry, self.sdk.service,
                                       self.sdk.awareness)
        self.init_done = False
        self.lazy_init_ttl = 0.1
        self.lazy_init_failures = 0

        threading.Timer(self.lazy_init_ttl, self.lazy_init).start()  # schedule the lazy_init method in 100 milliseconds
        _logger.info("M360 middleware loaded")

    def handle_request(self, request):
        _logger.debug("M360 middleware intercepted request: [" + request.method + "] " + request.path)
        query = request.GET if self.framework == "django" else request.args

        try:
            # check if this route is one of the reserved ones, if so handle it
            return self.handle_special_routes(request.path, query)
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def singleton(framework, default_config, config=None):
        """Access the singleton"""

        if Helper._instance:
            return Helper._instance

        if not Helper._instance:
            _logger.debug("Creating middleware helper instance")
            Helper._instance = Helper(framework, default_config, config)

        return Helper._instance

    @staticmethod
    def init_config(default_config, config=None):
        """
        Builds the final config object by using defaults for non provided keys
        """
        if not config:
            config = default_config
            return config
        for k, v in default_config.items():
            if k not in config.keys():
                config.setdefault(k, v)
        return config

    def lazy_init(self):
        try:
            if self.init_done:
                return
            self.sdk.auto_register(self.config)
            self.init_done = True
            _logger.info("M360 middleware registered successfully")
        except Exception as e:
            self.lazy_init_failures += 1
            if self.lazy_init_failures <= 5:
                _logger.debug("M360 middleware registration failed, retrying in a bit...")
                self.lazy_init_ttl = self.lazy_init_ttl * 3
                threading.Timer(self.lazy_init_ttl, self.lazy_init).start()  # retry in a bit
            else:
                _logger.error(str(e))
                raise Exception("M360 middleware failed to register with the gateway")

    def handle_special_routes(self, path, query):
        if path not in constants.RESERVED_ROUTES:
            return None
        if path == "/heartbeat":
            return {
                "name": self.app_name,
                "heartbeat": True
            }
        if path == "/registry/reload":
            ignore_list = query.getlist("ignoreList") if query and query.getlist("ignoreList") else []
            return self.maintenance.reload_registry(ignore_list)
        if path == "/awareness/reload":
            ignore_list = query.getlist("ignoreList") if query and query.getlist("ignoreList") else []
            return self.maintenance.reload_awareness(ignore_list)
        return None

def helper_instance(framework, default_config, config=None):
    """Get the singleton instance of the registry"""
    _logger.debug("calling Helper instance, os.pid=%d", os.getpid())
    return Helper.singleton(framework, default_config, config)
