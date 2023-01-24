import json
import os
import pickle

import redis

from redissimple.exception import RedisSimpleException
from redissimple.response_codes import ResponseCode

REDIS_CONF = {
    'host': os.getenv('REDIS_HOST') or '127.0.0.1',
    'port': os.getenv('REDIS_PORT') or 6379
}
if os.getenv('IS_ELASTIC_CACHE') is None:
    REDIS_CONF['password'] = os.getenv('REDIS_PASSWORD')


class RedisSimple():
    """Provide CRUD operations for redis cache."""

    def __init__(self):
        self.conn = self.connect()

    @classmethod
    def create_key(cls, tenant_id, entity_name, entity_id):
        key = os.getenv("APPLICATION_ENV") + "/" + str(tenant_id) + '/' + entity_name.upper() + '/' + str(
            entity_id)
        print('key ', key)
        return key

    @classmethod
    def connect(cls):
        try:
            print('In Class RedisAmplify  : ENTER connect()')
            print(REDIS_CONF['host'], REDIS_CONF['port'], REDIS_CONF['password'])
            if REDIS_CONF['password']:
                print('with password')
                return redis.Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], password=REDIS_CONF['password'])
            else:
                return redis.Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'], db=0)
        except Exception as e:
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))

    @classmethod
    def get(cls, tenant_id, entity_name, entity_id):
        print('in Get method')
        try:
            key = cls.create_key(tenant_id, entity_name, entity_id)
            rs = RedisSimple()
            data = rs.conn.get(key)
            if data:
                print('Returning json')
                return json.loads(data)
            else:
                raise RedisSimpleException(ResponseCode.KEY_NOT_FOUND,
                                           ResponseCode.getResponseMsg(ResponseCode.KEY_NOT_FOUND))

        except redis.ConnectionError as e:
            print(e)
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))
        finally:
            rs = None

    @classmethod
    def getResultSet(cls, tenant_id, entity_name, sql_query):
        print('in Get method')
        try:
            key_name = cls.create_key(tenant_id, entity_name, sql_query)
            key = pickle.dumps(key_name)
            rs = RedisSimple()
            result_set = rs.conn.get(key)
            data = pickle.loads(rs.get(key))
            if data:
                print('Returning resultset deserialized object')
                return json.loads(data)
            else:
                raise RedisSimpleException(ResponseCode.KEY_NOT_FOUND,
                                           ResponseCode.getResponseMsg(ResponseCode.KEY_NOT_FOUND))

        except redis.ConnectionError as e:
            print(e)
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))
        finally:
            rs = None

    @classmethod
    def set(cls, tenant_id, entity_name, entity_id, data, expiry_time=86400):
        print('In Class RedisSimple  : ENTER Method set')
        try:
            return_value = False
            rs = RedisSimple()
            key = cls.create_key(tenant_id, entity_name, entity_id)
            rs.conn.set(key, data, expiry_time)
            print('set done')
            return_value = True
            return return_value, key 
        except redis.ConnectionError as e:
            print(e)
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))
        finally:
            rs = None

    @classmethod
    def setResultSet(cls, tenant_id, entity_name, sql_query, result_set, expiry_time=86400):
        print('In Class RedisSimple  : ENTER Method set')
        try:
            return_value = False
            rs = RedisSimple()
            key_name = cls.create_key(tenant_id, entity_name, sql_query)
            key = pickle.dumps(key_name)
            data = pickle.dumps(result_set)
            rs.conn.set(key, data, expiry_time)
            print('set done')
            return_value = True
            return return_value, key
        except redis.ConnectionError as e:
            print(e)
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))
        finally:
            rs = None

    @classmethod
    def remove(cls, tenant_id, entity_name, entity_id):
        try:
            key = cls.create_key(tenant_id, entity_name, entity_id)
            rs = RedisSimple()
            rs.conn.delete(key)
            return True
        except redis.ConnectionError as e:
            print(e)
            raise RedisSimpleException(ResponseCode.CONNECTION_ERROR,
                                       ResponseCode.getResponseMsg(ResponseCode.CONNECTION_ERROR))
        finally:
            rs = None
