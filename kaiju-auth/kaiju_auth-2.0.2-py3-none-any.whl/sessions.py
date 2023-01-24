"""
This module contains various session management classes.

Classes
-------

"""

from __future__ import annotations

import asyncio
import time
import uuid
from datetime import datetime, timedelta
from typing import Union, List, Optional, Collection

try:
    from typing import TypedDict
except ImportError:
    # python 3.6 compatibility
    from typing_extensions import TypedDict

import sqlalchemy as sa
from aiohttp.web import Request, Response
from aiohttp_session import AbstractStorage, Session, SESSION_KEY
from aiohttp_session import setup as session_storage_setup

from kaiju_tools.cache import BaseCacheService
from kaiju_tools.serialization import dumps, loads
from kaiju_tools.services import ContextableService
from kaiju_db.services import DatabaseService

from .models import *

__all__ = ('SessionService', 'HTTPSessionService', 'UserSession')


class UserSession(Session):

    def __init__(self, *args, **kws):
        super().__init__(*args, **kws)
        if 'data' not in self._mapping:
            self._mapping['data'] = {}

    def __setitem__(self, key, value):
        self._mapping['data'][key] = value
        self._changed = True

    def __getitem__(self, key):
        if key in self._mapping:
            return self._mapping[key]
        else:
            return self._mapping['data'][key]


class SessionService(ContextableService):
    """
    Base session service which manages sessions in cache and in database.

    :param app:
    :param database_service:
    :param cache_service:
    :param max_age: session TTL
    :param logger:
    """

    class SessionDict(TypedDict):
        """Type hinting for session dictionary."""

        id: str
        iat: int
        exp: int
        max_age: int
        user_id: uuid.UUID
        permissions: List[str]
        data: dict  #: usually contains user settings or other arbitrary data

    service_name = 'sessions'
    table = session_table = sessions
    database_service_class = DatabaseService
    cache_service_class = BaseCacheService
    MAX_AGE = 3600 * 24  #: default max session age
    CACHE_KEY_PREFIX = 'session'

    def __init__(
            self, app,
            database_service: Union[str, database_service_class] = None,
            cache_service: Union[str, cache_service_class] = None,
            max_age=MAX_AGE, logger=None):
        ContextableService.__init__(self, app=app, logger=logger)
        self._cache_service_name = cache_service
        self._db = self.discover_service(database_service, cls=self.database_service_class)
        self.session_table = self._db.add_table(self.session_table)
        self._max_age = max(60, int(max_age))
        self._cache: BaseCacheService = None

    async def init(self):
        await self._delete_expired_sessions()
        self._cache = self.discover_service(self._cache_service_name, cls=self.cache_service_class)

    def create_empty_session(self, data: dict = None):
        """Returns a new empty (guest) session."""
        return self.create_session(user_id=None, permissions=None, data=data)

    async def create_session(
            self, id=None, user_id: Optional[uuid.UUID] = None,
            permissions: Optional[Collection[str]] = None,
            data: dict = None, store_always=False) -> SessionDict:
        """
        Initializes a new session and stores it in the cache and in the db.

        :param user_id: user identifier, if None, then it's a guest session
        :param permissions: list of user permissions
        :param store_always: session will be stored even if it doesn't contain a user id
        :param data: optional user data (settings, etc)
        """
        session = self._create_session(id, user_id, permissions, data)
        if user_id or store_always:
            await self._store_new_session(session)
        return session

    async def _store_new_session(self, session: dict):
        sql = self.table.insert().values(
            id=session['id'],
            created=datetime.fromtimestamp(session['iat']),
            data=session,
            expires=datetime.fromtimestamp(session['exp'])
        )
        await asyncio.gather(
            self._db.execute(sql),
            self._cache_session(session)
        )

    def _create_session(self, id, user_id, permissions, data):
        if not id:
            id = str(uuid.uuid4())
        iat = datetime.now()
        exp = iat + timedelta(seconds=self._max_age)
        if permissions is None or user_id is None:
            permissions = []
        session = {
            'id': id,
            'iat': int(iat.timestamp()),
            'exp': int(exp.timestamp()),
            'max_age': self._max_age,
            'user_id': user_id,
            'stored': True,
            'permissions': permissions,
        }
        if data:
            session['data'] = data
        else:
            session['data'] = {}
        return session

    async def load_session(self, session_id: Union[str, uuid.UUID]) -> Optional[SessionDict]:
        """Returns an existing session by its id."""

        session = await self._load_from_cache(session_id)
        if not session:
            sql = sa.select([self.session_table.c.data]).where(self.session_table.c.id == session_id)
            session = await self._db.fetchrow(sql)
            if session:
                return session['data']
        return session

    async def save_session(self, session: SessionDict) -> SessionDict:
        """Stores a modified session in the database."""
        if not session or not session.get("id"):
            return
        exp = datetime.now() + timedelta(seconds=self._max_age)
        session['exp'] = int(exp.timestamp())
        sql = self.table.update().where(
            self.session_table.c.id == session['id']
        ).values(
            data=session,
            expires=exp
        )
        await asyncio.gather(
            self._db.execute(sql),
            self._cache_session(session)
        )
        return session

    async def delete_session(self, session_id: Union[str, uuid.UUID]):
        """Removes an existing session completely."""

        sql = self.session_table.delete().where(self.session_table.c.id == session_id)
        await self._db.execute(sql)
        await self._delete_session_from_cache(session_id)

    def _create_caching_key(self, session_id: Union[str, uuid.UUID]) -> str:
        key = f'{self.CACHE_KEY_PREFIX}{BaseCacheService.DELIMITER}{session_id}'
        return key

    async def _cache_session(self, session: SessionDict):
        key = self._create_caching_key(session['id'])
        ttl = session['max_age'] * 1000
        try:
            await self._cache.set(key, session, ttl=ttl)
        except Exception as exc:
            self.logger.error('Caching error: "%s"', exc)

    async def _load_from_cache(self, session_id: Union[str, uuid.UUID]) -> SessionDict:
        key = self._create_caching_key(session_id)
        try:
            session = await self._cache.get(key)
            # if session:
            #     session = loads(session)
        except Exception as exc:
            self.logger.error('Caching error: "%s"', exc)
        else:
            return session

    async def _delete_session_from_cache(self, session_id: Union[str, uuid.UUID]):
        key = self._create_caching_key(session_id)
        try:
            await self._cache.delete(key)
        except Exception as exc:
            self.logger.error('Caching error: "%s"', exc)

    async def _delete_expired_sessions(self):
        sql = self.session_table.delete().where(
            self.session_table.c.expires <= datetime.now())
        await self._db.execute(sql)


class HTTPSessionService(AbstractStorage, ContextableService):
    """
    Session service adapter for aiohttp sessions.

    .. attention::

        You shouldn't redefine 'create', 'load', 'get', 'delete' methods here,
        at least not their intefraces, because they are all used by aiohttp
        backend. See `AbstractStorage` interface for detail.

    :param app:
    :param session_service:
    :param default_session_storage: if True (default) then this session service
        will be registered as default session storage in the supplied aiohttp app
    :param logger:
    :param args: goes to AbstractStorage
    :param kws: goes to AbstractStorage
    """

    service_name = 'http_sessions'
    session_service_class = SessionService
    DEFAULT_SESSION_STORAGE = True
    session_class = UserSession

    def __init__(
            self, app,
            session_service: Union[str, session_service_class] = None,
            *args, default_session_storage=DEFAULT_SESSION_STORAGE,
            logger=None, **kws):
        AbstractStorage.__init__(self, *args, encoder=dumps, decoder=loads, **kws)
        ContextableService.__init__(self, app=app, logger=logger)
        self._session_service_name = session_service
        self._session_service: SessionService = None
        if self.app and default_session_storage:
            session_storage_setup(app, self)

    async def init(self):
        self._session_service = self.discover_service(self._session_service_name, cls=self.session_service_class)

    @property
    def max_age(self) -> int:
        return self._session_service._max_age

    async def get_session(self, request: Request) -> UserSession:
        """
        Returns a session stored in a request. If session is not present,
        the method will create a new one
        """

        session = request.get(SESSION_KEY)
        if session is None:
            session = await self.load_session(request)
            if not session:
                session = await self._session_service.create_empty_session()
                session = self._wrap_session(session, new=True)
            request[SESSION_KEY] = session
        return session

    async def create_session(
            self, request: Request, user_id: Optional[str],
            permissions: Optional[List[str]], data: dict, store_always: bool = False) -> UserSession:
        """
        Create a completely new session and store it in db and in request.
        Usually it is used on login to create a fresh user session with
        meaningful data.
        """

        session = await self._session_service.create_session(
            id=None, user_id=user_id, permissions=permissions, data=data, store_always=store_always)
        session = self._wrap_session(session, new=True)
        request[SESSION_KEY] = session
        return session

    async def load_session(self, request: Request) -> Optional[UserSession]:
        """Loads an existing session by session id and writes it into the request."""

        session_id = self.load_cookie(request)
        if session_id:
            session_data = await self._session_service.load_session(session_id)
            if session_data:

                changed = False

                if all((
                    session_data['exp'] > time.time(),
                    session_data['exp'] < time.time() + self._session_service._max_age * 0.25
                )):
                    session_data['iat'] = int(time.time())
                    session_data['exp'] = int(time.time() + self._session_service._max_age)
                    changed = True

                session = self._wrap_session(session_data, new=False)
                session._changed = changed
                request[SESSION_KEY] = session
                return session

    async def save_session(self, request: Request, response: Response, session: UserSession):
        """Saves an existing session."""

        await self._session_service.save_session(session._mapping)
        self.save_cookie(
            response,
            str(session.identity),
            max_age=session.max_age
        )

    async def delete_session(self, request: Request):
        """Removes a session."""

        session = await self.get_session(request)
        if session:
            await self._session_service.delete_session(session.identity)
            session.clear()
            del request[SESSION_KEY]

    async def delete_cookie(self, response: Response):
        response.del_cookie(self._cookie_name)

    @classmethod
    def _wrap_session(cls, session_data: SessionService.SessionDict, new: bool = False) -> UserSession:
        session = cls.session_class(
            identity=session_data['id'],
            data={
                'created': session_data['iat'],
                'session': session_data
            },
            max_age=session_data['max_age'],
            new=new
        )
        return session
