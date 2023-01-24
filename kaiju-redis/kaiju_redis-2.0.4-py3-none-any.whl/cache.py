import textwrap
from typing import Awaitable

from kaiju_tools.cache import BaseCacheService

from .transport import RedisTransportService

__all__ = ['RedisCacheService']


class RedisCacheService(BaseCacheService):
    """Provides caching via Redis or KeyDB."""

    M_SET_EXP_SCRIPT = """
    local ttl = ARGV[1]
    for i, key in pairs(KEYS) do
        redis.call('SETEX', key, ttl, ARGV[i + 1])
    end
    """

    M_EXISTS_SCRIPT = """
    local result = {}
    for i, key in pairs(KEYS) do
        result[i] = redis.call('EXISTS', key)
    end
    return result
    """

    transport_cls = RedisTransportService
    _m_set_exp_script = None  #: compiled script
    _m_exists_script = None  #: compiled script
    _transport: RedisTransportService = None

    async def init(self):
        await super().init()
        self._m_set_exp_script = self._transport.register_script(textwrap.dedent(self.M_SET_EXP_SCRIPT))
        self._m_exists_script = self._transport.register_script(textwrap.dedent(self.M_EXISTS_SCRIPT))

    def _exists(self, key: str) -> Awaitable:
        return self._transport.exists([key])

    def _m_exists(self, *keys: str) -> Awaitable:
        return self._m_exists_script.execute(keys=keys)

    def _get(self, key: str) -> Awaitable:
        return self._transport.get(key)

    def _m_get(self, *keys: str) -> Awaitable:
        return self._transport.mget(keys)

    def _set(self, key: str, value, ttl: int) -> Awaitable:
        if ttl:
            return self._transport.setex(key, value, ttl)
        else:
            return self._transport.set(key, value)

    def _m_set(self, keys: dict, ttl: int) -> Awaitable:
        if ttl:
            return self._m_set_exp_script.execute(keys=list(keys.keys()), args=[ttl, *list(keys.values())])
        else:
            return self._transport.mset(keys)

    def _delete(self, key: str) -> Awaitable:
        return self._transport.delete([key])

    async def _m_delete(self, *keys: str):
        self.logger.info('DELETE')
        try:
            await self._transport.delete(keys)
        except Exception as exc:
            self.logger.info(str(exc))
        self.logger.info('OK')

    async def lpush(
        self,
        key: str,
        *values,
        use_serializer: bool = False,
        ignore_conn_errors: bool = BaseCacheService.IGNORE_CONN_ERRORS,
        nowait: bool = BaseCacheService.NOWAIT,
    ) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        _key = self._create_key(key)
        self.logger.info('Add key "%s" -> "%s".', key, _key)
        values = [self._dump_value(v, use_serializer) for v in values]

        if nowait:
            await self._queue.put(self._transport.lpush, (_key, values))
        else:
            await self._wrap_exec(self._transport.lpush(_key, values), ignore_conn_errors)

    async def rpush(
        self,
        key: str,
        *values,
        use_serializer: bool = False,
        ignore_conn_errors: bool = BaseCacheService.IGNORE_CONN_ERRORS,
        nowait: bool = BaseCacheService.NOWAIT,
    ) -> None:
        """Set a list data into list.

        :param key: string only
        :param values: list of serializable value
        :param use_serializer: use a serializer for value encoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        :param nowait: set operation in background (don't wait for response)
        """
        _key = self._create_key(key)
        self.logger.info('Add key "%s" -> "%s".', key, _key)
        values = [self._dump_value(v, use_serializer) for v in values]
        if nowait:
            await self._queue.put(self._transport.rpush, (_key, values))
        else:
            await self._wrap_exec(self._transport.rpush(_key, values), ignore_conn_errors)

    async def llen(self, key: str, ignore_conn_errors: bool = BaseCacheService.IGNORE_CONN_ERRORS) -> int:
        """Get count of list.

        :param key: string only
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        _key = self._create_key(key)
        self.logger.info('Get key count "%s" -> "%s".', key, _key)
        return await self._wrap_exec(self._transport.llen(_key), ignore_conn_errors)

    async def lrange(
        self,
        key: str,
        start=0,
        end=10,
        use_serializer: bool = False,
        ignore_conn_errors=BaseCacheService.IGNORE_CONN_ERRORS,
    ):
        """Get values from list by key.

        :param key: string only
        :param start: positive int only
        :param end: positive int only
        :param use_serializer: use a serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        self.logger.info('Set range for key %s .', key)
        _key = self._create_key(key)
        values = await self._wrap_exec(self._transport.lrange(_key, start=start, stop=end), ignore_conn_errors)
        if values:
            values = [self._load_value(v, use_serializer) for v in values]
        return values

    async def lpop(
        self, key: str, use_serializer: bool = False, ignore_conn_errors=BaseCacheService.IGNORE_CONN_ERRORS
    ):
        """Get values from list by key.

        :param key: string only
        :param use_serializer: use a serializer for value decoding (False = return raw)
        :param ignore_conn_errors: set True to ignore connection errors and skip the operation
        """
        self.logger.info('Set range for key %s .', key)
        _key = self._create_key(key)
        value = await self._wrap_exec(self._transport.lpop(_key), ignore_conn_errors)
        if value:
            value = self._load_value(value, use_serializer)
        return value
