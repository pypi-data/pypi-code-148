import inspect

from gremlin_python.process.traversal import T

import turbindo
# import turbindo.database.impl.sqlite.methods
from turbindo.database.base_object import AbstractDataTable
# from turbindo.database.default import SPECIAL_TYPES
from turbindo.database.impl.gremlin import Gremlin
from turbindo.log.logger import Logger
# from turbindo.runtime.exceptions import NoRowFoundException
# from turbindo.util import get_object_type_map


class GraphDataTable(AbstractDataTable):
    logger: Logger = Logger("GraphDataTable")

    @staticmethod
    def is_native_type(type_name) -> bool:
        return type_name in Gremlin.GRAPH_NATIVE_TYPE_LIST

    @staticmethod
    def get_serializer(type_name) -> callable:
        return Gremlin.GRAPH_TYPE_SERIALIZERS[type_name]

    @staticmethod
    async def _read(dataobj, primary_key):
        return Gremlin.g.V(primary_key).next()

    @staticmethod
    async def _set(dataobj, primary_key, **kwargs):
        tablename = dataobj.__class__.__name__

        annotation_types = get_object_type_map(dataobj.__class__)

        used_column_values = {}
        for k, v in kwargs.items():
            if not GraphDataTable.is_native_type(annotation_types[k]):
                serialize = GraphDataTable.get_serializer(annotation_types[k])
                if v != SPECIAL_TYPES.NOT_SET:
                    v = serialize(v)
            if v is not SPECIAL_TYPES.NOT_SET:
                used_column_values[k] = v

        exists = True
        try:
            await turbindo.database.impl.gremlin.Gremlin.g.V(primary_key).next()
        except NoRowFoundException:
            exists = False

        if not exists:
            turbindo.database.impl.gremlin.Gremlin.g.addV(tablename, T.id, primary_key).propertyies(**kwargs)
        else:
            turbindo.database.impl.gremlin.Gremlin.g.V(primary_key).properties(**kwargs)

    @staticmethod
    async def _delete(dataobj, primary_key):
        turbindo.database.impl.gremlin.Gremlin.g.V(primary_key).drop()

    @staticmethod
    async def _truncate(cls):
        turbindo.database.impl.gremlin.Gremlin.g.V.hasLabel(cls.__name__).drop().iterate()

    @staticmethod
    async def _dump(cls):
        return turbindo.database.impl.gremlin.Gremlin.g.V.hasLabel(cls.__name__)

    @staticmethod
    async def _dumpKeys(cls):
        return turbindo.database.impl.gremlin.Gremlin.g.V.hasLabel(cls.__name__).id()
