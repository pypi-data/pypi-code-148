"""basic utility microservices for Federated Secure Computing"""

from federatedsecure.server.builtins.util.kvstorage import KeyValueStorage


def federatedsecure_register(registry):

    registry.register(
        {
            "namespace": "federatedsecure",
            "plugin": "Util",
            "version": "0.6.0",
            "microservice": "KeyValueStorage"
        },
        KeyValueStorage()
    )
