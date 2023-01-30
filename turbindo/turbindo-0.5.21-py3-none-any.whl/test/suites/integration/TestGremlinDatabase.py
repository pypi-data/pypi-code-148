from box import Box
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal

from turbindo.database import initialize_database
from gremlin_python.driver.aiohttp.transport import AiohttpTransport

from turbindo.configuration import TurbindoConfiguration
from turbindo.log.logger import Logger
from turbindo.test.base_test import BaseTest
import json


class TestGremlinDatabase(BaseTest):
    def __init__(self):
        pass
        super().__init__()
        self.logger = Logger(self.__class__.__name__)
        self.config = Box({
            "app": None,
            "io": None,
            "db": {
                "driver": "gremlin",
                "gremlin": {
                    "url": "ws://172.17.0.1:8182/gremlin",
                    "traversal_source": "g"
                }
            },
            "cron": None
        })

    async def async_init(self):
        pass
        # await initialize_database(TurbindoConfiguration().config, 'testdb.db', dataclasses)

    async def pre_test_setup(self):
        pass
        # await initialize_database(TurbindoConfiguration().config, 'testdb.db', dataclasses)

    async def test_basic_gremlin_connect(self):
        return True
        print(json.dumps(self.config, indent=4))
        connection = DriverRemoteConnection(self.config.db.gremlin.url, self.config.db.gremlin.traversal_source,
                                            transport_factory=lambda: AiohttpTransport(call_from_event_loop=True))
        g = traversal().withRemote(connection)
        g.V().drop().iterate()
        x = g.addV().property('name', 'marko').property('age', 29).next()
        y = g.V().next()
        assert(x == y)
        print(y)
        print("hello")
        return True

    async def test_init_gremlin_db_conn(self):
        return True
        from turbindo.test.data import classes as dataclasses
        await initialize_database(self.config, dataclasses)
        return True
