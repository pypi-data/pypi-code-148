import importlib

from django.conf import settings

PLUGINS = {}

for plugin in settings.PLUGINS.get("MONITORING_SOURCES").get("INSTALLED", []):
    full_module_name = f"monitoring.plugins.sources.{plugin.lower()}"
    mymodule = importlib.import_module(full_module_name)
    PLUGINS[plugin] = mymodule.Plugin()
