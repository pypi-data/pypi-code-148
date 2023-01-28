"""routines to discover plugins and their microservices on server startup"""

import importlib
import pkgutil

import federatedsecure.server.builtins
import federatedsecure.server.plugins


def discover_builtins_and_plugins(registry):
    """discover microservices and classes in federatedsecure.server.builtins and federatedsecure.server.plugins"""

    for namespace_package in [federatedsecure.server.builtins, federatedsecure.server.plugins]:
        for _, name, _ in pkgutil.iter_modules(namespace_package.__path__,
                                               namespace_package.__name__ + "."):
            module = importlib.import_module(name)
            try:
                getattr(module, "federatedsecure_register")(registry)
            except AttributeError:
                pass
