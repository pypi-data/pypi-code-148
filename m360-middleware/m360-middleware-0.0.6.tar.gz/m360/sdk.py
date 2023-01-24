"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import logging

from m360 import constants, user, rbac, tenant, service, registry, awareness, validator, utils
from m360.gateway import connector

logging.basicConfig(level=constants.LOG_LEVEL)
_logger = logging.getLogger(__name__)
_connector = connector.instance()

class SDK(object):
    """Offers sdk related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        # set the logger
        self.logger = logging.getLogger("M360")
        # expose SDK libraries
        self.validator = validator.instance()
        self.awareness = awareness.instance()
        self.user = user.instance()
        self.rbac = rbac.instance()
        self.tenant = tenant.instance()
        self.service = service.instance()
        self.registry = registry.registry_instance()
        self.database = registry.database_instance()
        self.resource = registry.resource_instance()
        self.custom = registry.custom_registry_instance()
        self.app_name = None
        self.app_type = None
        self.config = None
        _logger.debug("SDK created")

    @staticmethod
    def sdk_singleton():
        """Access the singleton receiver"""

        if SDK._instance:
            return SDK._instance

        if not SDK._instance:
            _logger.debug("Creating sdk instance")
            SDK._instance = SDK()

        return SDK._instance

    def init(self, config):
        """
        Initialize the middleware and validate the provided configuration
        @param config {dict}
        """
        _logger.info("Initializing M360 SDK with the following config:")
        _logger.info(str(config))
        # SSL checks
        if not os.environ.get("APP_SSL_KEY") or not os.environ.get("APP_SSL_CERT"):
            _logger.error("""
\nError: Missing Application Private SSL certificate/key pair.
Please provide the paths to both the SSL certificate and its key either using environment variables ('APP_SSL_CERT' and 'APP_SSL_KEY')
\n#########################################################################################
\nIf you don't have a certificate/key pair, you can use openssl to generate one.
Example:\n> openssl req -new -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout /user/privatekey.key -out /user/certificate.crt
\nReference: https://www.baeldung.com/openssl-self-signed-cert
\n#########################################################################################\n
            """)
            self.exit_app()

        try:
            # load contract if a path was specified
            if config.get("contract") and type(config.get("contract")) is str:
                config["contract"] = utils.json_file_to_dict(config.get("contract"))

            # validate config schema
            _logger.debug("Validating configuration schema")
            self.validator.validate(config, "middleware")
            _logger.debug("Configuration schema is valid")

            if config.get("platform") in ["docker", "kubernetes"]:
                if not config.get("platformOptions") or type(config.get("platformOptions")) is not dict:
                    raise Exception("Missing 'platformOptions' for platform " + config.get("platform") +
                                    ". Please refer to documentation for additional help")
                errors = []
                if config.get("platform") == "docker":
                    # 'network': 'mike',
                    # 'service': 'service-express',
                    if not config.get("platformOptions").get("network"):
                        errors.append("Missing docker 'network' name in platform options")
                    if not config.get("platformOptions").get("service"):
                        errors.append("Missing docker 'service' name in platform options")
                else:  # == kubernetes
                    # 'namespace': 'mike',
                    # 'service': 'service-express',
                    # 'exposedPort': os.environ["APP_PORT"] or 4002,
                    if not config.get("platformOptions").get("namespace"):
                        errors.append("Missing docker 'namespace' value in platform options")
                    if not config.get("platformOptions").get("service"):
                        errors.append("Missing docker 'service' name in platform options")
                    if not config.get("platformOptions").get("exposedPort"):
                        errors.append("Missing docker 'exposedPort' value for container in platform options")

                if len(errors) > 0:
                    raise Exception("\n".join(errors))

            # check if preserved routes are overridden
            for api_object in config.get("contract").get("apis").values():
                for method, api_route in api_object.items():
                    for route_path in api_route.keys():
                        if method.lower() == "get" and route_path in constants.RESERVED_ROUTES:
                            raise Exception("Route [GET] " + route_path + " is reserved by the middleware, " +
                                            "please use a different route or method for your endpoint")

            # save local reference to config
            self.config = config
        except Exception as e:
            _logger.error(e)
            self.exit_app()

    def init_job(self, config):
        """
        Initialize the different libraries
        @param config {dict}
        """
        config["type"] = "job"
        config["server"] = {}

        self.init(config)

        _logger.info("Retrieving Service Contract from M360 Gateway")
        self.service.get(config.get("contract"))  # we just make sure there are no exceptions here
        _logger.info("Service Found in M360 Gateway")

        # initialize the middleware sdk gateway connector driver
        _connector.init(config.get("contract").get("name"), config.get("contract").get("version"))

        # get the registry from the gateway and cache it
        registry_data = self.registry.get()

        # if the registry was loaded...
        if registry_data:
            # initialize the awareness sdk module
            self.awareness.init(registry_data.get("_TTL"))
            _logger.info("Connection to M360 Gateway established")
            _logger.info("Environment Registry loaded from M360 Gateway and cached")

        # auto-wire the registry reload procedure with a default TTL of 30 seconds
        self.registry.auto_reload(30)

    def augment(self, config):
        """
        Augment the default configuration of the service contract and add the M360 maintenance routes to it.
        Augment the default microservice apis and add the M360 cloud awareness routes to the server instance.
        @param config {dict}
        """
        self.app_name = config.get("contract").get("name")
        self.app_type = config.get("type")

        # update the service contract with preserved maintenance entries
        config["contract"]["heartbeat"] = {
            "method": "get",
            "route": "/heartbeat",
            "access": False,
            "label": "Heartbeat"
        }
        config["contract"]["registry"] = {
            "method": "get",
            "route": "/registry/reload",
            "access": False,
            "label": "Reload Registry"
        }

        if not config.get("contract").get("apis").get("maintenance"):
            config["contract"]["apis"]["maintenance"] = {}
        if not config.get("contract").get("apis").get("maintenance").get("get"):
            config["contract"]["apis"]["maintenance"]["get"] = {}

        config["contract"]["apis"]["maintenance"]["get"]["/awareness/reload"] = {
            "access": False,
            "label": "Reload Cached Awareness"
        }

        self.rbac.set_service_config(config)

    def auto_register(self, config):
        """
        Method that triggers the auto registration procedure and registers/updates the microservice in the gateway.
        Once registered, the gateway will be able to proxy requests to it.
        @param config {dict}
        """
        # auto register the service at the gateway unless there's an env var set to stop it
        if constants.APP_AUTOREGISTER:
            self.service.ensure_ip_address(config)

            _logger.info("Registering/Updating Service Contract in M360 Gateway")
            response = self.service.register(config.get("contract"), config.get("ip"), config)
            _logger.info("Service Registered in M360 Gateway")

            # initialize the middleware sdk gateway connector driver
            _connector.init(config.get("contract").get("name"), config.get("contract").get("version"))

            # get the registry from the gateway and cache it
            registry_data = self.registry.get()

            if registry_data:  # if the registry was loaded..
                # initialize the awareness sdk module
                self.awareness.init(registry_data.get("_TTL"))

                # display all registration messages to the terminal
                if response and response.get("notifications") and len(response.get("notifications")) > 0:
                    _logger.info("\n*********************")
                    _logger.info("Registration Details:")
                    _logger.info("*********************")
                    _logger.info(str(response.get("notifications")))

                _logger.info("Connection to M360 Gateway established")
                _logger.info("Environment Registry loaded from M360 Gateway and cached")

            # auto-wire the registry reload procedure with a default TTL of 30 seconds
            self.registry.auto_reload(30)

    def stop_auto_reload(self):
        """
        Stops automatically reloading the registry (mainly useful for testing)
        """
        self.registry.stop_auto_reload()


    @staticmethod
    def exit_app():
        _logger.fatal("Exiting due to a fatal error")
        quit()

def instance():
    """Get the singleton instance of the sdk"""
    _logger.debug("calling instance, os.pid=%d", os.getpid())
    return SDK.sdk_singleton()
