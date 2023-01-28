from bson import ObjectId
from pymongo.cursor import Cursor
from pymongo.collection import Collection

from . import BaseModelManager
from ..context.mongo import MongoContext
from ..models.base import BaseModel


class MongoModelManager(BaseModelManager):
    def __init__(self, connection_string: str, database_name):
        super().__init__(connection_string, database_name)

    def _after(self, cursor: Cursor, **kwargs):
        if 'limit' in kwargs:
            cursor.limit(kwargs.get('limit'))

        if 'sort' in kwargs:
            if 'sortdirection' in kwargs:
                cursor.sort(kwargs.get('sort'), kwargs.get('sortdirection'))
            else:
                cursor.sort(kwargs.get('sort'))

        return cursor

    def find(self, column: Collection, query = {}, **kwargs):
        if 'select' in kwargs:
            return column.find(query, kwargs.get('select'))
        
        return column.find(query)

    def find_one(self, column: Collection, query = {}, **kwargs):
        if 'select' in kwargs:
            return column.find_one(query, kwargs.get('select'))
        
        return column.find_one(query)

    def exists(self, col: str, id: str):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            return column.count_documents({'_id': ObjectId(id)}) > 0

    def exists_where(self, col: str, query):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            return column.count_documents(query) > 0

    def get_one(self, col: str, id: str, **kwargs):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            query = {'_id': ObjectId(id)}
            return self.find_one(column, query, **kwargs)

    def get_all(self, col: str, **kwargs):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            cursor = self.find(column, **kwargs)
            return list(self._after(cursor, **kwargs))

    def get_many(self, col: str, query, **kwargs):
        with MongoContext(self.connection_string, self.database_name, col) as column:
            cursor = self.find(column, query, **kwargs)
            return list(self._after(cursor, **kwargs))

    def insert_one(self, item: BaseModel):
        with MongoContext(self.connection_string, self.database_name, item.classname) as column:
            result = column.insert_one(item.dict())
            item.id = result.inserted_id
            return item

    def update_one(self, update: BaseModel):
        with MongoContext(self.connection_string, self.database_name, update.classname) as column:
            query = {'_id': ObjectId(update.id) }
            column.update_one(query, {"$set": update.dict()})
            return update

    def delete_one(self, item: BaseModel):
        with MongoContext(self.connection_string, self.database_name, item.classname) as column:
            query = {'_id': ObjectId(item.id)}
            column.delete_one(query)
            return item
