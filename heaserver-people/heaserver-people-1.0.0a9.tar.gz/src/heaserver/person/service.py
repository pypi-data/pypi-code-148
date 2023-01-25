"""
The HEA Person Microservice is a wrapper around a Keycloak server for HEA to access user information. It accesses
Keycloak using an admin account. The default account is 'admin' with password of 'admin'. To configure this (and you
must do this to be secure!), add a Keycloak section to the service's configuration file with the following properties:
    Realm = the Keyclock realm from which to request user information.
    VerifySSL = whether to verify the Keycloak server's SSL certificate (defaults to True).
    Host = The Keycloak host (defaults to https://localhost:8444).
    Username = the admin account username (defaults to admin).
    Password = the admin account password.
    PasswordFile = the path to the filename with the password (overrides use of the PASSWORD property).

This microservice tries getting the password from the following places, in order:
    1) the KEYCLOAK_QUERY_USERS_PASSWORD property in the HEA Server Registry Microservice.
    2) the above config file.

If not present in any of those sources, a password of admin will be used.
"""
import logging

from heaserver.service import response
from heaserver.service.runner import init_cmd_line, routes, start, web, Configuration
from heaserver.service.wstl import action, builder_factory
from heaserver.service.db.mongo import MongoManager
from heaobject.person import Person
from heaserver.service import appproperty
from heaserver.service.client import get_property
from datetime import datetime, timedelta
from heaobject.root import ShareImpl, Permission
from heaobject.user import NONE_USER, ALL_USERS
from yarl import URL
from typing import Coroutine, Any, Callable
from aiohttp import ClientSession, ClientResponseError
from aiohttp.web import Request
from pathlib import Path
from warnings import warn

KEYCLOAK_QUERY_USERS_PASSWORD = 'KEYCLOAK_QUERY_USERS_PASSWORD'
MONGODB_PERSON_COLLECTION = 'people'
CONFIG_SECTION = 'Keycloak'
REALM = 'hea'
VERIFY_SSL = False
HOST = 'https://localhost:8444'
USERNAME = 'admin'
PASSWORD = None
PASSWORD_FILE = None

@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/people/{id}')
@action(name='heaserver-people-person-get-properties', rel='hea-properties')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_person(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    ---
    summary: A specific person.
    tags:
        - heaserver-people-get-person
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    session = request.app[appproperty.HEA_CLIENT_SESSION]
    access_token, token_type = await _get_access_token_and_token_type(request, session)
    try:
        person = await _get_user(access_token, session, token_type, request.match_info['id'])
    except ClientResponseError as e:
        if e.status == 404:
            person = None
        else:
            return response.status_internal_error();
    return await response.get(request, person.to_dict() if person else {})


@routes.get('/people/byname/{name}')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_person_by_name(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    ---
    summary: A specific person, by name.
    tags:
        - heaserver-people-get-person-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    logger = logging.getLogger(__name__)
    session = request.app[appproperty.HEA_CLIENT_SESSION]
    access_token, token_type = await _get_access_token_and_token_type(request, session)
    persons = await _get_users(access_token, session, token_type, params={'username': request.match_info['name']})
    return await response.get(request, persons[0].to_dict() if persons else None)


@routes.get('/people')
@routes.get('/people/')
@action(name='heaserver-people-person-get-properties', rel='hea-properties')
@action(name='heaserver-people-person-get-self', rel='self', path='/people/{id}')
async def get_all_persons(request: web.Request) -> web.Response:
    """
    Gets all persons.
    :param request: the HTTP request.
    :return: all persons.
    ---
    summary: All persons.
    tags:
        - heaserver-people-get-all-persons
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    logger = logging.getLogger(__name__)
    session = request.app[appproperty.HEA_CLIENT_SESSION]
    logger.debug('headers: ' + str(request.headers))
    access_token, token_type = await _get_access_token_and_token_type(request, session)
    persons = await _get_users(access_token, session, token_type)
    return await response.get_all(request, [person.to_dict() for person in persons])


def main() -> None:
    config = init_cmd_line(description='Read-only wrapper around Keycloak for accessing user information.',
                           default_port=8080)
    _parse_config(config)
    start(db=MongoManager, config=config, wstl_builder_factory=builder_factory(__package__))


def _parse_config(config: Configuration):
    """
    Parses data from the config file's Keycloak section.

    :param config: the configuration data (required).
    """
    global REALM, VERIFY_SSL, HOST, USERNAME, PASSWORD, PASSWORD_FILE
    config_data = config.parsed_config if config else None
    if config_data and CONFIG_SECTION in config_data:
        _section = config_data[CONFIG_SECTION]
        REALM = _section.get('Realm', 'hea')
        VERIFY_SSL = _section.getboolean('VerifySSL', True)
        HOST = _section.get('Host', 'https://localhost:8444')
        USERNAME = _section.get('Username', 'admin')
        PASSWORD = _section.get('Password', None)
        PASSWORD_FILE = _section.get('PasswordFile', None)


def _keycloak_user_to_person(user: dict[str, Any]) -> Person:
    """
    Converts a user JSON object from Keycloak to a HEA Person object.

    :param user: a Keycloak user object as a JSON dict.
    :return: a Person object.
    """
    person = Person()
    person.id = user['id']
    person.name = user['username']
    person.first_name = user.get('firstName')
    person.last_name = user.get('lastName')
    person.email = user.get('email')
    person.created = datetime.fromtimestamp(user['createdTimestamp'] / 1000.0)
    person.owner = NONE_USER
    share = ShareImpl()
    share.user = ALL_USERS
    share.permissions = [Permission.VIEWER]
    person.shares = [share]
    return person


def _get_access_token_and_token_type_getter() -> Callable[[Request, ClientSession], Coroutine[Any, Any, tuple[str, str]]]:
    """
    Factory that returns a callable for requesting an access token and token type from Keycloak.

    :return: a callable. Pass the HTTP Requst and ClientSession into it to get an access token.
    """
    latest_token_time: datetime | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    refresh_expires_in: int | None = None
    access_token: str | None = None
    token_type: str | None = None

    async def _get_access_token_and_token_type_(request: Request, session: ClientSession) -> tuple[str, str]:
        """
        Request an access token from Keycloak.

        :param request: the HTTP request (required).
        :param session: the client session (required).
        :return: a two-tuple containing the access token and token type.
        """
        nonlocal refresh_token, expires_in, refresh_expires_in, latest_token_time, access_token, token_type
        logger = logging.getLogger(__name__)

        def refresh_token_body(refresh_token: str):
            return {
                'client_id': 'admin-cli',
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token
            }

        token_url = URL(HOST) / 'auth' / 'realms' / 'master' / 'protocol' / 'openid-connect' / 'token'
        if latest_token_time is not None and \
            expires_in is not None and access_token is not None and token_type is not None and \
            (datetime.now() + timedelta(seconds=30) < (latest_token_time + timedelta(seconds=expires_in))):
            logger.debug('Reusing access token')
            return access_token, token_type
        else:
            access_token = None
            token_type = None
            if refresh_token is not None and refresh_expires_in is not None and latest_token_time is not None and \
                (datetime.now() + timedelta(seconds=30)) < (latest_token_time + timedelta(seconds=refresh_expires_in)):
                logger.debug('Requesting new access token using refresh token')
                async with session.post(token_url, data=refresh_token_body(refresh_token), verify_ssl=VERIFY_SSL) as response_:
                    latest_token_time = datetime.now()
                    content = await response_.json()
                    logging.getLogger(__name__).debug(f'content {content}')
                    access_token = content['access_token']
                    token_type = content['token_type']
                    return access_token, token_type
            else:
                logger.debug('Requesting new access token using credentials')
                refresh_token = None
                password_property = await get_property(request.app, KEYCLOAK_QUERY_USERS_PASSWORD)
                if password_property is not None:
                    password = password_property.value
                    logger.debug('Read password from registry service')
                elif PASSWORD_FILE:
                    password = Path(PASSWORD_FILE).read_text()
                    logger.debug('Read password from file')
                elif PASSWORD:
                    password = PASSWORD
                    logger.debug('Read password from config')
                else:
                    password = 'admin'
                    warn('Using default password!!!')
                token_body = {
                    'username': USERNAME,
                    'password': password,
                    'client_id': 'admin-cli',
                    'grant_type': 'password'
                }
                async with session.post(token_url, data=token_body, verify_ssl=VERIFY_SSL) as response_:
                    latest_token_time = datetime.now()
                    content = await response_.json()
                    logging.getLogger(__name__).debug(f'content {content}')
                    access_token = content['access_token']
                    refresh_token = content['refresh_token']
                    expires_in = content['expires_in']
                    refresh_expires_in = content['refresh_expires_in']
                    token_type = content['token_type']
                return access_token, token_type
    return _get_access_token_and_token_type_


_get_access_token_and_token_type = _get_access_token_and_token_type_getter()


async def _get_users(access_token: str, session, token_type: str, params: dict[str, str] | None = None) -> list[Person]:
    """
    Gets a list of users from Keycloak using the '/auth/admin/realms/{realm}/users' REST API call.

    :param access_token: the access token to use (required).
    :param session: the client session (required).
    :param token_type: the token type (required).
    :param params: any query parameters to add to the users request.
    :return: a list of Person objects, or the empty list if there are none.
    """
    logger = logging.getLogger(__name__)
    users_url = URL(HOST) / 'auth' / 'admin' / 'realms' / REALM / 'users'
    if params:
        users_url_ = users_url.with_query(params)
    else:
        users_url_ = users_url
    async with session.get(users_url_,
                           headers={'Authorization': f'{token_type} {access_token}', 'cache-control': 'no-cache'},
                           verify_ssl=VERIFY_SSL) as response_:
        response_.raise_for_status()
        user_json = await response_.json()
        logger.debug(f'Response was {user_json}')
        persons = []
        for user in user_json:
            person = _keycloak_user_to_person(user)
            persons.append(person)
    return persons


async def _get_user(access_token: str, session: ClientSession, token_type: str, id_: str) -> Person:
    """
    Gets the user from Keycloak with the given id using the '/auth/admin/realms/{realm}/users/{id}' REST API call.

    :param access_token: the access token to use (required).
    :param session: the client session (required).
    :param token_type: the token type (required).
    :param id_: the user id (required).
    :return: a Person object.
    :raises ClientResponseError if an error occurred or the person was not found.
    """
    logger = logging.getLogger(__name__)
    user_url = URL(HOST) / 'auth' / 'admin' / 'realms' / REALM / 'users' / id_
    async with session.get(user_url,
                           headers={'Authorization': f'{token_type} {access_token}', 'cache-control': 'no-cache'},
                           verify_ssl=VERIFY_SSL) as response_:
        user_json = await response_.json()
        logger.debug(f'Response was {user_json}')
        return _keycloak_user_to_person(user_json)
