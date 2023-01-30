import json

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.process.graph_traversal import GraphTraversalSource
from turbindo.configuration import TurbindoConfiguration


class Gremlin:
    GRAPH_NATIVE_TYPE_LIST = ["bool", "str", "int"]
    GRAPH_TYPE_SERIALIZERS = {
        "datetime": lambda dt: dt.timestamp(),
        "list": lambda lst: json.dumps(lst),
        "dict": lambda dct: json.dumps(dct),
        "EntryType": lambda et: int(et)
    }

    config = TurbindoConfiguration().config

    @classmethod
    @property
    def g(cls) -> GraphTraversalSource:
        return traversal().withRemote(DriverRemoteConnection(
            cls.config.db.gremlin.url,
            cls.config.db.gremlin.traversal_source
        ))
