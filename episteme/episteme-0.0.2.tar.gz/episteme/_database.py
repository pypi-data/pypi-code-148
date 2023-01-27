from __future__ import annotations

import functools
from typing import final
from urllib.parse import urlparse

from pymongo import MongoClient

from episteme._credentials import creds


@final
class _Database:
    def __init__(self) -> None:
        self.client = None
        self.db = None
        self.connect()

    def get_database(self):
        connection_string = creds('db')
        con = urlparse(connection_string)
        if con.path in ['', '/']:
            db = 'episteme-db'
        else:
            db = con.path[1:]
        return self.client[db]

    def connect(self):
        connection_string = creds('db')
        try:
            self.client = MongoClient(connection_string)
            self.db = _MongoDB
            # print(self.client.server_info())
        except Exception as e:
            print('oops')
            print(e)

    def insert(self, model_name, data, pk):
        self.db.insert(self.get_database(), model_name, data, pk)

    def update(self, model_name, data, pk):
        self.db.update(self.get_database(), model_name, data, pk)

    def find(self, model_name, id, pk):
        return self.db.find(self.get_database(), model_name, id)


@final
class _MongoDB():

    def _fix_id_write(data, pk):
        if '_id' not in data:
            data['_id'] = data[pk]
            del data[pk]
        return data

    def _fix_id_read(data, pk):
        if '_id' not in data:
            data[pk] = data['_id']
            del data['_id']
        return data

    def find(client: MongoClient, collection, id, pk):
        collection_name = client[collection]
        result = collection_name.find_one({'_id': id})
        if result is None:
            return None
        return _MongoDB.fix_id_read(result, pk)

    def insert(client: MongoClient, collection, data, pk):
        collection_name = client[collection]
        _MongoDB._fix_id_write(data, pk)
        collection_name.insert_one(data)

    def update(client: MongoClient, collection, data, pk):
        pass
        # collection_name = client[collection]
        # _MongoDB._fix_id_write(data, pk)
        # collection_name.update(data)

    def delete():
        pass


@functools.lru_cache(maxsize=1)
def get_db():
    return _Database()
