"""
Login service is an endpoint for all user session operations. It can combine
multiple methods of authentication and session management.

There are three other services it may depend on:

- :class:`.UserService` - stores user/group data
- :class:`.HTTPSessionService` - stateful session management
- :class:`.JWTService` - this service can create, sign and validate JWT tokens

For example, we can define a fully functional service able to create tokens
and provide user methods and stored sessions as well.

.. code-block:: python

    my_login_service = HTTPLoginService(
        app=my_app,
        user_service=my_user_service,
        session_service=my_session_service,
        token_service=my_jwt_service,
        logger=my_app_logger
    )

Or you can create a simple token verification service which uses a shared cache
to verify tokens signatures but doesn't provide login/user methods. It may be
useful for microservices.

.. code-block:: python

    my_login_service = HTTPLoginService(
        app=my_app,
        user_service=False,
        session_service=False,
        token_service=my_jwt_service,
        logger=my_app_logger
    )

.. attention::

    Shared cache is essential in the latter case, because if a service can't
    access users/sessions table it should at least be able to read shared
    public RSA keys to verify token signatures. Otherwise all received tokens
    will be automatically marked as invalid.


Classes
-------

"""

import asyncio
import time
from typing import Optional, TypedDict, Union

from aiohttp.web import Request

from kaiju_tools.functions import retry
from kaiju_tools.exceptions import NotAuthorized, Conflict, APIException
from kaiju_tools.services import ContextableService
from kaiju_tools.rpc.client import RPCClientService, AbstractTokenInterface
from kaiju_tools.rpc.abc import Session
from kaiju_tools.rpc import AbstractRPCCompatible

from .users import UserService
from .tokens import JWTService
from .sessions import HTTPSessionService

__all__ = (
    'HTTPLoginService', 'ErrorCodes', 'JWTClientService'
)


class ErrorCodes:
    AUTH_METHOD_DISABLED = 'auth.auth_method_disabled'
    CANNOT_RECEIVE_TOKEN = 'auth.cannot_receive_token'


class HTTPLoginService(ContextableService, AbstractRPCCompatible):
    """User service what is compatible with `HTTPCompatibleJSONQueueServer`
    rpc service.

    It is used for session/cookie based authentication and profile management.

    :param app: web app
    :param session_service: http session service instance or name
    :param user_service: user management service name or instance
    :param session_refresh_interval: user permissions stored in session's
    cache will be refreshed periodically, this parameter determines the
    refresh interval (in seconds), you shouldn't use too short intervals
    because it slows the request performance
    :param permissions: custom RPC permissions
    :param logger:
    """

    class _H_TokenResponse(TypedDict):
        access: str
        refresh: str
        exp: int
        refresh_exp: int

    service_name = 'auth'
    session_service_class = HTTPSessionService
    token_service_class = JWTService
    user_service_class = UserService
    ErrorCodes = ErrorCodes
    SESSION_REFRESH_INTERVAL = 300
    _session_refresh_key = 'updated'

    def __init__(
            self, app,
            user_service: Union[str, user_service_class] = None,
            session_service: Union[str, session_service_class] = None,
            token_service: Union[str, token_service_class] = None,
            session_refresh_interval: int = SESSION_REFRESH_INTERVAL,
            permissions: dict = None,
            logger=None):

        super().__init__(app=app, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)
        self._session_refresh_interval = session_refresh_interval
        self._user_service_name = user_service
        self._session_service_name = session_service
        self._token_service_name = token_service
        self._user_service = None
        self._session_service = None
        self._token_service = None

    @property
    def fake_routes(self):
        """Fake routes. They are used for faking RPC in requests that need an
        actual HTTP request object in input."""

        if self.user_backend_enabled and self.session_backend_enabled:
            routes = {
                f'{self.service_name}.register': self.register,
                f'{self.service_name}.login': self.login,
                f'{self.service_name}.logout': self.logout,
                f'{self.service_name}.change_password': self.change_password
            }
        else:
            routes = {}

        return routes

    @property
    def routes(self):

        routes = {}

        if self.user_backend_enabled:
            routes['update_profile'] = self.update_profile
            routes['user_info'] = self.get_user

        if self.token_backend_enabled:
            routes['jwt_get'] = self.jwt_get
            routes['jwt_refresh'] = self.jwt_refresh

        return routes

    @property
    def permissions(self):
        return {
            self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_USER_PERMISSION,
            'jwt_get_by_user_id': self.PermissionKeys.GLOBAL_SYSTEM_PERMISSION,
            'jwt_get': self.PermissionKeys.GLOBAL_GUEST_PERMISSION,
            'jwt_refresh': self.PermissionKeys.GLOBAL_GUEST_PERMISSION
        }

    async def init(self):
        self._user_service = self.discover_service(
            self._user_service_name, cls=self.user_service_class, required=False)
        self._session_service = self.discover_service(
            self._session_service_name, cls=self.session_service_class, required=False)
        self._token_service = self.discover_service(
            self._token_service_name, cls=self.token_service_class, required=False)

    async def register(self, request: Request, username: str, email: str, password: str):
        """Registers a new user and performs a login."""

        self._check_user_service_is_available()
        self._check_session_service_is_available()
        await self._user_service.register(username, email, password)
        return await self.login(request, username, password)

    async def jwt_get_by_user_id(self, user_id, ttl=None) -> _H_TokenResponse:
        """
        This method creates a JWT token for a specific user. It can be used
        by the system to create some user level access tokens while not requiring
        the specific user to be actually logged in.

        .. attention::

            This method should not be exposed to non-system users.

        :param user_id: uuid
        :param ttl: token lifetime in seconds
        """

        self._check_user_service_is_available()
        self._check_token_service_is_available()
        user = await self._user_service.get_user_info_by_user_id(user_id)
        user['id'] = user_id
        return await self._create_tokens(user, ttl=ttl)

    async def jwt_get(self, username: str, password: str) -> _H_TokenResponse:
        """Logs user in and returns a JWT token pair."""

        self._check_user_service_is_available()
        self._check_token_service_is_available()
        user = await self._user_service.auth(username=username, password=password)
        return await self._create_tokens(user)

    async def _create_tokens(self, user_info: dict, ttl=None):
        data = {
            'user_id': user_info['id'],
            'permissions': user_info['permissions'],
        }
        access, refresh = await self._token_service.generate_token_pair(ttl=ttl, **data)
        return {
            'access': access.serialize(compact=True),
            'refresh': refresh.serialize(compact=True),
            'exp': access.claims_data['exp'],
            'refresh_exp': refresh.claims_data['exp']
        }

    async def jwt_refresh(self, refresh: str) -> _H_TokenResponse:
        """Refreshes an auth token using a refresh token."""

        self._check_token_service_is_available()
        access, refresh = await self._token_service.refresh_token(refresh)
        return {
            'access': access.serialize(compact=True),
            'refresh': refresh.serialize(compact=True),
            'exp': access.claims_data['exp'],
            'refresh_exp': refresh.claims_data['exp']
        }

    async def jwt_get_session(self, request: Request) -> Session:
        """
        Validates a JWT token and returns a user quasi-session if available.
        A guest session will be returned otherwise.
        """

        self._check_token_service_is_available()
        if self._token_service:
            token = self._extract_token(request)
            if token:
                token = await self._token_service.verify_token(token)
                session = token.claims_data
                return session
        return await self.get_guest_session()

    async def get_guest_session(self) -> Session:
        permissions = await self._user_service.get_default_nonlogin_permissions()
        return {
            'user_id': None,
            'permissions': permissions,
            #'stored': False,
            #'data': {}
        }

    async def login(self, request: Request, username: str, password: str):
        """Logs user in and creates a new session. If old user is currently present,
        it will log him out first."""

        self._check_user_service_is_available()
        self._check_session_service_is_available()
        session = await self.get_session(request)
        user = await self.get_user(session)
        if user:
            await self.logout(request)
        user = await self._user_service.auth(username=username, password=password)
        data = self._get_session_data(user)
        await self._session_service.delete_session(request)
        session = await self._session_service.create_session(
            request,
            user_id=user['id'],
            permissions=user['permissions'],
            data=data
        )
        session._changed = True
        return await self.get_user(session)

    async def logout(self, request: Request):
        """Logout an authorized user and clear the session."""

        self._check_session_service_is_available()
        session = await self.get_session(request)
        if await self.get_user(session):
            await self._session_service.delete_session(request)
        else:
            raise NotAuthorized('Authorization required.')

    async def change_password(self, request: Request, username: str, password: str, new_password: str):
        """Changes user password to a new one and performs a fresh login."""

        self._check_user_service_is_available()
        self._check_session_service_is_available()
        session = await self.get_session(request)
        if await self.get_user(session):
            await self._user_service.change_password(username, password, new_password)
            await self.logout(request)
            return await self.login(request, username, new_password)
        else:
            raise NotAuthorized('Authorization required.')

    async def update_profile(self, session: Session, settings: dict) -> dict:
        """Updates user profile metadata."""

        self._check_user_service_is_available()
        settings = await self._user_service.update_profile(session, settings)
        settings = settings['settings']
        session['settings'] = settings
        return settings

    async def get_user(self, session: Session):
        """Returns a complete information about the current logged user."""

        self._check_user_service_is_available()
        user_id = session.get('user_id')
        if user_id:
            return await self._user_service.get_user_info(session)

    async def get_session(self, request: Request):
        """Writes a user session and session permissions. Update permissions
        if required."""

        self._check_user_service_is_available()
        self._check_session_service_is_available()
        session = await self._session_service.get_session(request)
        user_id = session.get('user_id')

        if user_id:  # session has a real user
            last_updated = session.get('updated', 0)
            if last_updated + self._session_refresh_interval < time.time():
                data = await self._user_service._get_user_and_permissions(user_id)
                data = self._get_session_data(data)
                session._mapping.update(data)

        if session.get('permissions') is None:
            session['permissions'] = await self._user_service.get_default_nonlogin_permissions()

        return session

    @staticmethod
    def _get_session_data(user: dict) -> dict:
        return {
            'settings': user['settings'],
            'updated': int(time.time())
        }

    @property
    def session_backend_enabled(self) -> bool:
        return self._session_service_name is not False

    def _check_session_service_is_available(self):
        if not self._session_service:
            raise Conflict(
                'Session service is disabled.',
                service=self.service_name,
                code=self.ErrorCodes.AUTH_METHOD_DISABLED)

    @property
    def user_backend_enabled(self) -> bool:
        return self._user_service_name is not False

    def _check_user_service_is_available(self):
        if not self._user_service:
            raise Conflict(
                'User service is disabled.',
                service=self.service_name,
                code=self.ErrorCodes.AUTH_METHOD_DISABLED)

    @property
    def token_backend_enabled(self) -> bool:
        return self._token_service_name is not False

    def _check_token_service_is_available(self):
        if not self._token_service:
            raise Conflict(
                'Token service is disabled.',
                service=self.service_name,
                code=self.ErrorCodes.AUTH_METHOD_DISABLED)

    @staticmethod
    def has_token(request: Request):
        """Special method required by HTTP views."""

        if 'Authorization' in request.headers:
            return bool(request.headers['Authorization'])
        else:
            return False

    def _extract_token(self, request: Request) -> Optional[str]:
        """Extracts a JWT token from request headers if possible."""

        if self.has_token(request):
            auth_header = request.headers['Authorization'].strip()
            if auth_header.startswith('Bearer'):
                token = auth_header.replace('Bearer', '', 1).strip()
                if token:
                    return token


class JWTClientService(ContextableService, AbstractTokenInterface):
    """JWT token client - automatically acquires and refreshes JWT tokens.

    Usage example:

    Create a service or a service config for the client.

    .. code-block:: python

        jwt_client_settings = {
          'cls': 'JWTClientService',
          'settings': {
            'login_service': 'rpc_client_service_name',
            'auth': {
              'username': 'bob',
              'password': 'qwerty'
            }
          }
        }

    After the initialization you will be able to use it in your RPC clients
    or get tokens manually via `get_token` method:

    .. code-block:: python

        token = await jwt_client.get_token()
        my_client.call(headers={'Authorization': f'Bearer {token}'})

    Token lifetimes will be automatically monitored by the service.
    """

    class _AuthParams(TypedDict):
        username: str
        password: str

    _exp_window = 10

    def __init__(
            self, app,
            auth: _AuthParams,
            login_service: Union[str, HTTPLoginService, RPCClientService] = None,
            exp_window: int = _exp_window,
            retry_settings: dict = None,
            logger=None
    ):
        """Initialize.

        :param app: web app
        :param auth: login values (username, password)
        :param login_service: login service name or instance
        :param exp_window: token expiration window in seconds before its actual exp time
        :param retry_settings: token refresh and login `retry` settings
        :param logger: logger instance
        """
        super().__init__(app=app, logger=logger)
        self._exp_window = max(1, int(exp_window))
        self._login_service = login_service
        self._login_method = None
        self._refresh_method = None
        self._closing = False
        self._auth = auth
        self._tokens: HTTPLoginService._H_TokenResponse = None
        self._retry_settings = retry_settings if retry_settings else {}
        self._loop = None
        self._refresh_completed = asyncio.Event()
        self._refresh_completed.set()

    async def get_token(self) -> str:
        """Get a valid access token.

        :raises APIException: if token cannot be refreshed
        """
        if not self._refresh_completed.is_set():
            await self._refresh_completed.wait()
            if self._tokens:
                return self._tokens['access']

        self._refresh_completed.clear()
        try:
            if not self._tokens or self._refresh_token_expired():
                self.logger.info('Requesting a new token.')
                self._tokens = await retry(
                    self._login_method, logger=self.logger, **self._retry_settings)
                self.logger.info('Token updated.')
            elif self._access_token_expired():
                self.logger.info('Requesting a new token.')
                self._tokens = await retry(
                    self._refresh_method, logger=self.logger, **self._retry_settings)
                self.logger.info('Token updated.')
        except Exception as exc:
            self._tokens = None
            raise APIException(
                'Error while receiving a token.',
                base_exc=exc, code=ErrorCodes.CANNOT_RECEIVE_TOKEN)
        finally:
            self._refresh_completed.set()

        return self._tokens['access']

    async def init(self):
        """Initialize service."""
        # hack! setting jwt method according to login service type

        self._login_service = self.discover_service(
            self._login_service, cls=(HTTPLoginService, RPCClientService))

        if isinstance(self._login_service, HTTPLoginService):
            self._login_method = self._jwt_get_local
            self._refresh_method = self._jwt_refresh_local
        else:
            self._login_method = self._jwt_get
            self._refresh_method = self._jwt_refresh

        # load initial tokens and raise an exception if any

        await self.get_token()
        self._closing = False
        self._loop = asyncio.create_task(self._refresh_loop())

    async def close(self):
        """Terminate service."""
        self._closing = True
        await self._refresh_completed.wait()
        self._loop.cancel()
        self._loop = None
        self._tokens = None

    @property
    def closed(self) -> bool:
        return self._tokens is None

    async def _refresh_loop(self) -> None:
        while not self._closing:
            try:
                await self.get_token()
            except APIException as exc:
                self.logger.error('Error while background refreshing tokens.', exc_info=exc)
                sleep_interval = 1.
            else:
                sleep_interval = min(self._tokens['exp'], self._tokens['refresh_exp'])
            await asyncio.sleep(self._get_dt(sleep_interval))

    def _access_token_expired(self) -> bool:
        return self._get_dt(self._tokens['exp']) <= 0

    def _refresh_token_expired(self) -> bool:
        return self._get_dt(self._tokens['refresh_exp']) <= 0

    def _get_dt(self, exp: float) -> float:
        return max(0.0, float(exp) - self._exp_window - time.time())

    async def _jwt_get(self) -> HTTPLoginService._H_TokenResponse:
        result = await self._login_service.call(
            method=f'{HTTPLoginService.service_name}.jwt_get',
            params=self._auth, raise_exception=True,
            headers={'Authorization': ''})
        return result

    async def _jwt_refresh(self) -> HTTPLoginService._H_TokenResponse:
        result = await self._login_service.call(
            method=f'{HTTPLoginService.service_name}.jwt_refresh',
            params={'refresh': self._tokens['refresh']}, raise_exception=True,
            headers={'Authorization': f'Bearer {self._tokens["access"]}'})
        return result

    async def _jwt_get_local(self) -> HTTPLoginService._H_TokenResponse:
        result = await self._login_service.jwt_get(**self._auth)
        return result

    async def _jwt_refresh_local(self) -> HTTPLoginService._H_TokenResponse:
        result = await self._login_service.jwt_refresh(refresh=self._tokens['refresh'])
        return result
