"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import os
import logging
import threading

from m360 import constants
from m360.gateway import connector
from m360.ttlcache import TTLCache

_logger = logging.getLogger(__name__)
_connector = connector.instance()
_cache = TTLCache(ttl=300)  # TTL defaults to 5 minutes

class Registry(object):
    """
    Registry class that fetches, caches and reloads the registry information of the environment by invoking the
    maintenance gateway API
    """

    # singleton
    _instance = None

    _registry_reload_timer = None

    def __init__(self):
        _logger.debug("Registry created")

    @staticmethod
    def registry_singleton():
        """Access the singleton receiver"""

        if Registry._instance:
            return Registry._instance

        if not Registry._instance:
            _logger.debug("Creating registry instance")
            Registry._instance = Registry()

        return Registry._instance

    @classmethod
    def __get_registry_section(cls, registry, section=None):
        """
        Returns registry[section] if it's there or registry if it isn't
        @param registry {dict}
        @param section  {str}
        @returns {dict} The specific registry section
        """
        if not registry:
            return None
        if section and type(section) is str and section.strip() and registry.get(section):
            return registry.get(section)
        return registry

    @classmethod
    def get(cls, section=None):
        """
        Returns the cached registry data
        If the cache is empty, it calls load, then it returns the result
        If the parameter is provided, it returns the specified portion of the registry
        @param section {str}
        @returns {dict} The registry record
        """
        registry = _cache.get("registry")
        if registry:
            return cls.__get_registry_section(registry, section)
        # load registry to continue
        cls.load()
        registry = _cache.get("registry")
        return cls.__get_registry_section(registry, section)

    @classmethod
    def clear(cls):
        """
        Clears the whole cache
        """
        _cache.clear()

    @staticmethod
    def load():
        """
        Calls the maintenance gateway API and caches the retrieved registry
        """
        delay = 0.001 if constants.MW_TESTING else constants.DEFAULT_RETRY_DELAY_SEC
        data = _connector.invoke({
            "method": "get",
            "route": "/registry/",
            "retryOnFailure": 3,
            "retryDelay": delay
        })
        # cache the retrieved info
        if data and isinstance(data, dict) and data.get("registry"):
            ttl = data.get("registry").get("_TTL") / 1000
            _cache.set("registry", data.get("registry"), ttl)
            _cache.set("custom", data.get("custom"), ttl)
            _cache.set("resources", data.get("resources"), ttl)
            _cache.set("databases", data.get("databases"), ttl)

        return True

    @classmethod
    def auto_reload(cls, ttl):
        """
        Starts a thread that handles reloading the registry periodically
        @param ttl {int}    Time to live in seconds, time between reloads
        """
        registry = _cache.get("registry")
        if registry and registry.get("_TTL"):
            ttl = registry.get("_TTL") / 1000
        _logger.info("Next registry reload in " + str(ttl) + " seconds...")

        def _reload():
            """Runs when the timer expires"""
            cls.load()
            cls.auto_reload(ttl)

        # cancel any running timers
        cls.stop_auto_reload()
        # schedule the _reload method in TTL seconds
        cls._registry_reload_timer = threading.Timer(ttl, _reload)
        cls._registry_reload_timer.start()

    @classmethod
    def reload(cls):
        """
        Calls load() and returns the latest registry
        """
        cls.load()
        return _cache.get("registry")

    @classmethod
    def stop_auto_reload(cls):
        """
        Stops any running timers
        """
        try:
            if cls._registry_reload_timer:
                cls._registry_reload_timer.cancel()
        except Exception:
            pass

class CustomRegistry(object):
    """Offers custom registry related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Custom registry created")

    @staticmethod
    def custom_registry_singleton():
        """Access the singleton receiver"""

        if CustomRegistry._instance:
            return CustomRegistry._instance

        if not CustomRegistry._instance:
            _logger.debug("Creating custom registry instance")
            CustomRegistry._instance = CustomRegistry()

        return CustomRegistry._instance

    @classmethod
    def get(cls, name=None):
        """
        Returns the requested custom registry based on its name
        @param name {str}
        @returns {dict} The custom_registry record
        """
        custom_registries = _cache.get("custom")
        if custom_registries and type(custom_registries) is dict and len(custom_registries) > 0:
            if name and name.strip():
                return custom_registries.get(name)
            else:
                return custom_registries
        return None

class Resource(object):
    """Offers resource related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Resource created")

    @staticmethod
    def resource_singleton():
        """Access the singleton receiver"""

        if Resource._instance:
            return Resource._instance

        if not Resource._instance:
            _logger.debug("Creating resource instance")
            Resource._instance = Resource()

        return Resource._instance

    @classmethod
    def get(cls, name=None):
        """
        Returns the requested resource based on its name
        @param name {str}
        @returns {dict} The resource record
        """
        resources = _cache.get("resources")
        if resources and type(resources) is dict and len(resources) > 0:
            if name and name.strip():
                return resources.get(name)
            else:
                return resources
        return None

class Database(object):
    """Offers database related helper methods"""

    # singleton
    _instance = None

    def __init__(self):
        _logger.debug("Database created")

    @staticmethod
    def database_singleton():
        """Access the singleton receiver"""

        if Database._instance:
            return Database._instance

        if not Database._instance:
            _logger.debug("Creating database instance")
            Database._instance = Database()

        return Database._instance

    @classmethod
    def __fix_db_name(cls, db_type, main, prefixed, tenant_code):
        """
        Format the DB name based on whether it's a single tenant or multi-tenant DB
        """
        if db_type == "multitenant":
            prefix = prefixed.replace(main, "") if main else prefixed
            if prefix == prefixed:
                if main:
                    return tenant_code + "_" + main
                else:
                    return tenant_code + "_" + prefix
            else:
                return prefix + tenant_code + "_" + main
        else:
            return prefixed

    @classmethod
    def __get_db(cls, db_type, name, tenant_code):
        """
        Load the specific database info from the cache by name
        """
        databases = _cache.get("databases")
        if databases and type(databases) is dict and databases.get(db_type):
            if name and name.strip() and databases.get(db_type).get(name):
                db = databases.get(db_type).get(name)
                cluster_name = db.get("cluster")
                db["cluster"] = resource_instance().get(cluster_name)
                if not db.get("cluster"):
                    db["cluster"] = {}
                db["cluster"]["name"] = cluster_name
                db["name"] = cls.__fix_db_name(db_type, name, db.get("name"), tenant_code)
                return db
            else:
                for db_name in databases.get(db_type):
                    cluster_name = databases.get(db_type).get(db_name).get("cluster")
                    databases[db_type][db_name]["cluster"] = resource_instance().get(cluster_name)
                    if not databases[db_type][db_name]["cluster"]:
                        databases[db_type][db_name]["cluster"] = {}
                    databases[db_type][db_name]["cluster"]["name"] = cluster_name
                    inner_db_name = databases.get(db_type).get(db_name).get("name")
                    databases[db_type][db_name]["name"] = cls.__fix_db_name(db_type, name, inner_db_name, tenant_code)
                return databases.get(db_type)
        return None

    @classmethod
    def get(cls, db_type, name=None, tenant_code=None):
        """
        Returns the requested database based on its name and db_type.
        If the database is multi-tenant, the tenant_code parameter is required to populate the DB name.
        @param db_type      {str}
        @param name         {str}
        @param tenant_code  {str}
        @returns {dict} The database record
        """
        if db_type == "single":
            return cls.__get_db("single", name, tenant_code)
        elif db_type == "multitenant":
            if not tenant_code or (type(tenant_code) is str and not tenant_code.strip()):
                return None
            else:
                return cls.__get_db("multitenant", name, tenant_code)
        else:
            return None

def registry_instance():
    """Get the singleton instance of the registry"""
    _logger.debug("calling registry_instance, os.pid=%d", os.getpid())
    return Registry.registry_singleton()

def custom_registry_instance():
    """Get the singleton instance of the custom_registry"""
    _logger.debug("calling custom_registry_instance, os.pid=%d", os.getpid())
    return CustomRegistry.custom_registry_singleton()

def resource_instance():
    """Get the singleton instance of the resource"""
    _logger.debug("calling resource_instance, os.pid=%d", os.getpid())
    return Resource.resource_singleton()

def database_instance():
    """Get the singleton instance of the database"""
    _logger.debug("calling database_instance, os.pid=%d", os.getpid())
    return Database.database_singleton()
