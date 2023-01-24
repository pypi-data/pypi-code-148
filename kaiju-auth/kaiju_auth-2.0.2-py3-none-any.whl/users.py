from __future__ import annotations

import asyncio
import random
import re
import uuid
from typing import Union, List, FrozenSet, Dict, Optional, Collection

try:
    from typing import TypedDict
except ImportError:
    # python 3.6 compatibility
    from typing_extensions import TypedDict

import bcrypt
import sqlalchemy as sa

import kaiju_tools.jsonschema as j
from kaiju_tools.exceptions import ValidationError, Conflict, NotAuthorized
from kaiju_tools.rpc.abc import AbstractRPCCompatible, ServerSessionFlag
from kaiju_tools.services import Contextable
from kaiju_db.services import DatabaseService, SQLService

from .etc import WEAK_PASSWORDS
from .models import *

__all__ = (
    'PermissionService', 'GroupService', 'UserService'
)


class SessionData(TypedDict):
    user_id: uuid.UUID
    permissions: frozenset
    settings: dict


class PermissionService(SQLService, Contextable, AbstractRPCCompatible):
    """
    Service which stores user permission keys and information about them.

    See `.SQLService` for more information.

    :param app: web app
    :param database_service: db service instance or name
    :param permissions: custom RPC permissions
    :param logger: logger instance
    """

    class _TaggedPermissions(TypedDict):
        tag: Optional[str]
        permissions: List[dict]

    service_name = 'permissions'
    table = permission_table = permissions
    update_columns_blacklist = {'id'}

    def __init__(
            self, app,
            database_service: Union[SQLService.database_service_class, str] = None,
            permissions: dict = None, logger=None):
        super().__init__(app=app, database_service=database_service, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)

    @property
    def routes(self) -> dict:
        return {
            **super().routes,
            'get_all': self.get_all_permissions
        }

    @property
    def validators(self):
        return {
            **super().validators,
            'get_all': j.Object({'group_by_tag': j.Boolean()})
        }

    async def get_all_permissions(self, group_by_tag=True, id=None, query=None) -> Union[List[dict], List[_TaggedPermissions]]:
        """
        Returns all active permissions in alphabetic order.

        :param group_by_tag: permissions will be grouped by a permission tag
        :param query: search by permission tag or description
        """
        conditions = [
            self.permission_table.c.enabled == True
        ]

        if query:
            conditions.append(sa.func.lower(self.permission_table.c.description).op('~')(sa.func.lower(query)))
            conditions.append(sa.func.lower(self.permission_table.c.id).op('~')(sa.func.lower(query)))

        if id:
            if type(id) is not list:
                id = [id]

            conditions.append(self.permission_table.c.id.in_(id))

        sql = self.permission_table.select().where(
            sa.and_(*conditions)
        ).order_by(self.permission_table.c.tag, self.permission_table.c.id)
        data = await self._db.fetch(sql)
        # data = self._filter_columns(data, self.select_columns)
        if group_by_tag:
            result = {}
            for row in data:
                tag = row['tag']
                if tag in result:
                    result[tag].append(row)
                else:
                    result[tag] = [row]
            data = [
                {
                    'tag': tag,
                    'permissions': _permissions
                }
                for tag, _permissions in result.items()
            ]
        return data


class GroupService(SQLService, Contextable, AbstractRPCCompatible):
    """
    This service stores information about user groups and their permissions.

    See `.SQLService` for more information.

    :param app: web app
    :param database_service: db service instance or name
    :param permission_service: permissions service instance or name
    :param permissions: custom RPC permissions
    :param logger: logger instance
    """

    class _GroupPermissions(TypedDict):
        id: str
        permissions: FrozenSet[str]

    service_name = 'user_groups'
    db_service_class = DatabaseService
    permission_service_class = PermissionService
    table = groups_table = groups
    group_permissions_table = group_permissions
    permissions_table = permissions
    update_columns_blacklist = {'id'}

    def __init__(
            self, app, database_service: Union[DatabaseService, str] = None,
            permission_service: Union[PermissionService, str] = None,
            permissions: dict = None, logger=None):

        super().__init__(app=app, database_service=database_service, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)
        self._db.add_table(self.group_permissions_table)
        self.permissions_table = self.permission_service_class.table
        self._permission_service_name = permission_service
        self._permission_service: PermissionService = None

    @property
    def routes(self) -> dict:
        return {
            **super().routes,
            'permissions.get': self.get_permissions,
            'permissions.set': self.set_permissions,
            'permissions.update': self.modify_permissions
        }

    async def init(self):
        self._permission_service = self.discover_service(
            self._permission_service_name, cls=self.permission_service_class)
        self.permissions_table = self._permission_service.table

    async def get_permissions(self, id: Union[str, List[str]]) -> Union[frozenset, List[_GroupPermissions]]:
        """
        Returns group(s) permissions. Non-active permission keys will be ignored.

        :param id: group identifier
        :returns: a set of permissions
        """

        if isinstance(id, Collection) and not type(id) is str:
            if not id:
                return []

            sql = sa.select([
                self.group_permissions_table.c.group_id,
                self.group_permissions_table.c.permission_id
            ]).select_from(
                self.group_permissions_table.join(
                    self.permissions_table,
                    sa.and_(
                        self.group_permissions_table.c.permission_id == self.permissions_table.c.id,
                    )
                )
            ).where(
                sa.and_(
                    self.group_permissions_table.c.group_id.in_(id),
                    self.permissions_table.c.enabled == True
                )
            )
            rows = await self._db.fetch(sql)
            _groups = {group_id: [] for group_id in id}
            for row in rows:
                _groups[row['group_id']].append(row['permission_id'])
            result = [
                {
                    'id': group_id,
                    'permissions': frozenset(_permissions)
                }
                for group_id, _permissions in _groups.items()
            ]
        else:
            sql = sa.select([
                self.group_permissions_table.c.permission_id
            ]).select_from(
                self.group_permissions_table.join(
                    self.permissions_table,
                    sa.and_(
                        self.group_permissions_table.c.permission_id == self.permissions_table.c.id,
                    )
                )
            ).where(
                sa.and_(
                    self.group_permissions_table.c.group_id == id,
                    self.permissions_table.c.enabled == True
                )
            )
            rows = await self._db.fetch(sql)
            result = frozenset(row['permission_id'] for row in rows)

        return result

    async def set_permissions(self, id: str, permissions: list) -> frozenset:
        """
        Sets permissions in the group.
        All non-mentioned permissions will be removed.

        :param id: group identifier
        :param permissions: a list of permissions
        :returns: a new set of available permissions
        """

        _permissions = set(permissions)
        _existing_permissions = await self.get_permissions(id)
        _to_delete = _existing_permissions.difference(_permissions)
        _to_add = _permissions.difference(_existing_permissions)
        tasks = []

        if _to_delete:
            sql = self.group_permissions_table.delete().where(
                sa.and_(
                    self.group_permissions_table.c.permission_id.in_(list(_to_delete)),
                    self.group_permissions_table.c.group_id == id
                )
            )
            tasks.append(self._db.execute(sql))

        if _to_add:
            sql = self.group_permissions_table.insert().values([
                {'group_id': id, 'permission_id': key}
                for key in _to_add
            ])
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)
        return frozenset(permissions)

    async def modify_permissions(self, id: str, permissions: Dict[str, bool]) -> frozenset:
        """
        Modifies permissions in a group.

        .. code-block:: python

            await groups.modify_permissions('users', {'do.this': True, 'do.that': False})

        :param id: group identifier
        :param permissions: { <permission key>: <bool> } mapping
        :returns: a new set of available permissions
        """

        if not permissions:
            return await self.get_permissions(id)

        keys = list(permissions.keys())
        sql_1 = self.permissions_table.select().where(
            self.permissions_table.c.id.in_(keys)
        )
        sql_2 = self.group_permissions_table.select().where(
            sa.and_(
                self.group_permissions_table.c.permission_id.in_(keys),
                self.group_permissions_table.c.group_id == id
            )
        )

        keys, existing_keys, _ = await asyncio.gather(
            self._db.fetch(sql_1),
            self._db.fetch(sql_2),
            self.get(id, columns=['id'])
        )

        keys = set((row['id'] for row in keys))
        existing_keys = set((row['permission_id'] for row in existing_keys))
        to_add, to_remove = [], []

        for permission_key, value in permissions.items():
            if permission_key in keys:
                if value and permission_key not in existing_keys:
                    to_add.append(permission_key)
                else:
                    to_remove.append(permission_key)

        tasks = []

        if to_remove:
            sql_1 = self.group_permissions_table.delete().where(
                sa.and_(
                    self.group_permissions_table.c.permission_id.in_(to_remove),
                    self.group_permissions_table.c.group_id == id
                )
            )
            tasks.append(self._db.execute(sql_1))
        data = [
            {'group_id': id, 'permission_id': permission_id}
            for permission_id in to_add
        ]
        if data:
            sql_2 = self.group_permissions_table.insert().values(data)
            tasks.append(self._db.execute(sql_2))

        await asyncio.gather(*tasks)
        return await self.get_permissions(id)


class UserService(SQLService, Contextable, AbstractRPCCompatible):
    """
    This service stores information about users and user groups.

    See `.SQLService` for more information.

    :param app: web app
    :param database_service: db service instance or name
    :param group_service: user group service instance or name
    :param default_group: default group to use for new registered users
    :param default_nonlogin_group: default group for guest users
    :param salt_rounds:
    :param min_password_len:
    :param max_password_len:
    :param min_username_len:
    :param max_username_len:
    :param weak_passwords: a list of weak (forbidden) passwords
    :param bad_password_timeout: time to wait between failed login attempts
    :param bad_password_timeout_jitter:
    :param permissions: custom RPC permissions
    """

    class ErrorCodes:

        RPC_PERMISSION_DENIED = 'auth.rpc.permission_denied'

        USER_NOT_FOUND = 'auth.user.not_found'
        USER_EXISTS = 'auth.user.exists'
        USER_AUTH_FAILED = 'auth.user.authentication_failed'
        USER_IDENTICAL_PASSWORDS_SUPPLIED = 'auth.user.identical_passwords_supplied'
        USER_INVALID_EMAIL = 'auth.user.invalid_email'
        USER_INVALID_USERNAME = 'auth.user.invalid_username'
        USER_WEAK_PASSWORD = 'auth.user.weak_password'
        USER_INVALID_PASSWORD = 'auth.user.invalid_password'

        GROUP_NOT_FOUND = 'auth.group.not_found'
        GROUP_EXISTS = 'auth.group.exists'
        GROUP_CANT_EDIT = 'auth.group.cant_edit'
        GROUP_CANT_DELETE = 'auth.group.cant_delete'
        GROUP_PARENT_NOT_FOUND = 'auth.group.parent_group_not_found'
        GROUP_CANT_INHERIT_ITSELF = 'auth.group.cant_inherit_itself'
        GROUP_CANT_HAVE_PARENT = 'auth.group.cant_have_parent'
        GROUP_PARENT_MUST_BE_SYSTEM = 'auth.group.parent_group_must_be_system_group'

        PERMISSION_NOT_FOUND = 'auth.permission.not_found'
        PERMISSION_EXISTS = 'auth.permission.exists'

    class _UserGroups(TypedDict):
        id: str
        groups: List[str]

    class _UserPermissions(TypedDict):
        id: str
        permissions: FrozenSet[str]

    service_name = 'users'
    db_service_class = DatabaseService
    group_service_class = GroupService
    table = users_table = users
    user_groups_table = user_groups

    salt_rounds = 13                    #: OWASP recommendation
    bad_password_timeout = 0.5          #: timeout in sec if auth failed
    bad_password_timeout_jitter = 0.5   #: timeout jitter in sec if auth failed

    min_password_len = 12               #: OWASP recommendation
    max_password_len = 128              #: OWASP recommendation
    password_regex = re.compile(rf'^(?=.*\d).{{{min_password_len},{max_password_len}}}$')

    min_username_len = 4
    max_username_len = 32
    username_regex = re.compile(rf'^[\w0-9_-]{{{min_username_len},{max_username_len}}}$')

    email_regex = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

    _username_regex = re.compile(username_regex)
    _password_regex = re.compile(password_regex)
    _email_regex = re.compile(email_regex)

    update_columns_blacklist = {'id'}
    select_columns_blacklist = {'password', 'salt'}

    def __init__(
            self, app, database_service: Union[DatabaseService, str] = None,
            group_service: Union[GroupService, str] = None,
            default_group: str = None,
            default_nonlogin_group: str = None,
            salt_rounds=salt_rounds,
            weak_passwords=None,
            min_password_len=min_password_len,
            max_password_len=max_password_len,
            min_username_len=min_username_len,
            max_username_len=max_username_len,
            bad_password_timeout=bad_password_timeout,
            bad_password_timeout_jitter=bad_password_timeout_jitter,
            permissions: dict = None,
            logger=None):
        super().__init__(app=app, database_service=database_service, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)
        self._group_service_name = group_service
        self._db.add_table(self.user_groups_table)
        self._default_group = default_group
        self._default_nonlogin_group = default_nonlogin_group
        if weak_passwords is None:
            self.weak_passwords = WEAK_PASSWORDS
        else:
            self.weak_passwords = frozenset(weak_passwords)
        self.salt_rounds = salt_rounds
        self.bad_password_timeout = bad_password_timeout
        self.bad_password_timeout_jitter = bad_password_timeout_jitter
        self.min_username_len = min_username_len
        self.max_username_len = max_username_len
        self.min_password_len = min_password_len
        self.max_password_len = max_password_len
        self._group_service: GroupService = None

    @property
    def routes(self) -> dict:
        return {

            **super().routes,
            'set_password': self.set_password,

            'groups.get': self.get_user_groups,
            'groups.set': self.set_user_groups,
            'groups.update': self.modify_user_groups,

            'permissions.get': self.get_user_permissions,
            'permissions.get_defaults': self.get_default_permissions,
            'permissions.get_nonlogin_defaults': self.get_default_nonlogin_permissions,

        }

    async def init(self):
        self._group_service = self.discover_service(self._group_service_name, cls=self.group_service_class)

    async def exists(self, id) -> Union[bool, frozenset]:
        """Checks if user with such id exists."""

        if isinstance(id, Collection) and not type(id) is str:
            sql = self.table.select().with_only_columns([
                self.table.c.is_active
            ]).where(
                self.table.c.id.in_(id)
            )
            rows = await self._db.fetch(sql)
            return frozenset((row['id'] for row in rows))
        else:
            sql = self.table.select().with_only_columns([
                self.table.c.is_active
            ]).where(
                self.table.c.id == id
            )
            user = await self._db.fetchrow(sql)
            return user is not None

    async def get_default_permissions(self) -> frozenset:
        """Returns a set of default user group permissions."""

        if self._default_group:
            return await self._group_service.get_permissions(self._default_group)
        else:
            return frozenset()

    async def get_default_nonlogin_permissions(self) -> frozenset:
        """Returns a set of guest user permissions."""

        if self._default_nonlogin_group:
            return await self._group_service.get_permissions(self._default_nonlogin_group)
        else:
            return frozenset()

    async def get_user_groups(self, id: str) -> _UserGroups:
        """Returns a list of groups of a user."""

        sql = self.user_groups_table.select().with_only_columns([
            self.user_groups_table.c.group_id
        ]).where(
            self.user_groups_table.c.user_id == id
        )
        rows = await self._db.fetch(sql)
        _groups = list((row['group_id'] for row in rows))
        if not _groups and self._default_group:
            _groups = [self._default_group]
        return {
            'id': id,
            'groups': _groups
        }

    async def set_user_groups(self, id: str, groups: list):
        """Sets groups for a user. All non-mentioned groups will be removed."""

        _groups = set(groups)
        _existing_groups = await self.get_user_groups(id)
        _existing_groups = set(_existing_groups['groups'])
        _to_delete = _existing_groups.difference(_groups)
        _to_add = _groups.difference(_existing_groups)
        tasks = []

        if _to_delete:
            sql = self.user_groups_table.delete().where(
                sa.and_(
                    self.user_groups_table.c.user_id == id,
                    self.user_groups_table.c.group_id.in_(list(_to_delete))
                )
            )
            tasks.append(self._db.execute(sql))

        if _to_add:
            sql = self.user_groups_table.insert().values([
                {'user_id': id, 'group_id': key}
                for key in _to_add
            ])
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)

    async def modify_user_groups(self, id: str, groups: Dict[str, bool]) -> _UserGroups:
        """Modify user groups."""

        if not groups:
            return await self.get_user_groups(id)

        keys = list(groups.keys())
        sql = self.user_groups_table.select().with_only_columns([
            self.user_groups_table.c.group_id
        ]).where(
            sa.and_(
                self.user_groups_table.c.user_id == id,
                self.user_groups_table.c.group_id.in_(keys)
            )
        )
        rows = await self._db.fetch(sql)
        existing_groups = set(row['group_id'] for row in rows)
        to_remove, to_add = [], []

        for group_id, value in groups.items():
            if value:
                if group_id not in existing_groups:
                    to_add.append(group_id)
            else:
                if group_id in existing_groups:
                    to_remove.append(group_id)

        tasks = []

        if to_add:
            data = [
                {
                    'user_id': id,
                    'group_id': group_id
                }
                for group_id in to_add
            ]
            sql = self.user_groups_table.insert().values(data)
            tasks.append(self._db.execute(sql))

        if to_remove:
            sql = self.user_groups_table.delete().where(
                sa.and_(
                    self.user_groups_table.c.user_id == id,
                    self.user_groups_table.c.group_id.in_(to_remove)
                )
            )
            tasks.append(self._db.execute(sql))

        await asyncio.gather(*tasks)
        return await self.get_user_groups(id)

    async def get_user_permissions(self, id) -> _UserPermissions:
        """Get user permissions."""

        _groups = await self.get_user_groups(id)
        if _groups:
            _permissions = await self._group_service.get_permissions(_groups['groups'])
            _permissions = set().union(*(_group['permissions'] for _group in _permissions))
            _permissions = frozenset(_permissions)
        else:
            _permissions = frozenset()

        return {
            'id': id,
            'permissions': _permissions
        }

    async def register(
            self, username: str, email: str, password: str,
            columns='*', **settings):
        """Adds a new user. Used by administrators or user managers."""

        self.validate_username(username)
        self.validate_email(email)
        password = self.validate_password(password)

        sql = self.table.select().where(
            sa.or_(
                self.table.c.username == username,
                self.table.c.email == email
            )
        )

        data = await self._db.fetchrow(sql)

        if data is not None:
            raise Conflict(
                'User or e-mail address is already registered.', key=username,
                code=self.ErrorCodes.USER_EXISTS)

        salt, password = self._hash_password(username, password)
        settings['username'] = username
        settings['email'] = email
        settings['password'] = password
        settings['salt'] = salt
        settings['id'] = uuid.uuid4()
        sql = self.table.insert().values(settings)
        await self._db.execute(sql)
        return await self._get_user_and_permissions(settings['id'], columns)

    def get_user_info(self, session: SessionData):
        user_id = session['user_id']
        return self.get_user_info_by_user_id(user_id)

    async def get_user_info_by_user_id(self, user_id):
        data = self.get(user_id, columns=['username', 'email', 'full_name', 'created', 'settings'])
        permissions = self.get_user_permissions(user_id)
        data, permissions = await asyncio.gather(data, permissions)
        permissions = permissions['permissions']
        return {
            **data,
            'permissions': permissions
        }

    async def get_profile(self, session: SessionData):
        user_id = session['user_id']
        data = await self.get(user_id, columns=['settings'])
        return {
            'id': user_id,
            'settings': data['settings']
        }

    async def update_profile(self, session: SessionData, settings: dict):
        user_id = session['user_id']
        data = await self.get(user_id, columns=['settings'])
        meta = data['settings']
        for key, value in settings.items():
            if value is None:
                if key in meta:
                    del meta[key]
            else:
                meta[key] = value
        sql = self.table.update().values(settings=meta).where(self.table.c.id == user_id)
        await self._db.execute(sql)
        return {
            'id': user_id,
            'settings': meta
        }

    async def auth(self, username: str, password: str, columns='*'):
        """User authorization."""

        sql = self.table.select().with_only_columns([
            self.table.c.id,
            self.table.c.password,
            self.table.c.salt
        ]).where(
            sa.and_(
                self.table.c.username == username,
                self.table.c.is_active == True,
                self.table.c.is_blocked == False
            )
        )
        user = await self._db.fetchrow(sql)

        if user is None:
            raise NotAuthorized(
                'User authentication failed.',
                code=self.ErrorCodes.USER_AUTH_FAILED)

        if not self._check_password(username, password, user['salt'], user['password']):
            raise NotAuthorized(
                'User authentication failed.',
                code=self.ErrorCodes.USER_AUTH_FAILED)

        return await self._get_user_and_permissions(user['id'], columns)

    async def change_password(self, username: str, password: str, new_password: str):

        if password == new_password:
            raise ValidationError(
                'Old password matches the new one.',
                code=self.ErrorCodes.USER_IDENTICAL_PASSWORDS_SUPPLIED)

        new_password = self.validate_password(new_password)
        user = await self.auth(username=username, password=password)
        await self.set_password(user['id'], username, new_password)
        return True

    async def set_password(self, id, username: str, password: str):
        salt, password = self._hash_password(username, password)
        sql = self.table.update().where(
            sa.and_(
                self.table.c.id == id,
                self.table.c.username == username
            )
        ).values(
            password=password,
            salt=salt
        )
        await self._db.execute(sql)

    def validate_email(self, email: str):
        if not self._email_regex.fullmatch(email):
            raise ValidationError(
                f'Enter a valid e-mail address.',
                key='email', value=None,
                code=self.ErrorCodes.USER_INVALID_EMAIL)

    def validate_username(self, username: str):
        if not self._username_regex.fullmatch(username):
            raise ValidationError(
                f'Username must be from {self.min_username_len} up to'
                f' {self.max_username_len} characters,'
                f' only letters, numbers and _ . - are allowed.',
                key='username', value=None,
                min_characters=self.min_username_len,
                max_characters=self.max_username_len,
                code=self.ErrorCodes.USER_INVALID_USERNAME)

    def validate_password(self, password: str):
        password = password.strip(' \n\t\r')
        if password in self.weak_passwords:
            raise ValidationError(
                f'Password is too weak or compromised.',
                key='password', value=None,
                code=self.ErrorCodes.USER_WEAK_PASSWORD)

        elif not self._password_regex.fullmatch(password):
            raise ValidationError(
                f'Password must contain {self.min_password_len} up to'
                f' {self.max_password_len} characters at least one of them'
                f' must be a digit.',
                key='password', value=None,
                min_characters=self.min_password_len,
                max_characters=self.max_password_len,
                code=self.ErrorCodes.USER_INVALID_PASSWORD)

        return password

    def _hash_password(self, username, password, salt=None) -> (bytes, bytes):
        if salt is None:
            salt = bcrypt.gensalt(self.salt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        if not self._check_password(username, password, salt, hashed):
            raise RuntimeError('Internal error.')
        return salt, hashed

    def _check_password(self, username, password, salt, hashed) -> bool:
        result = bcrypt.checkpw(password.encode('utf-8'), hashed)
        return result

    def _get_timeout(self):
        return random.random() * self.bad_password_timeout_jitter + self.bad_password_timeout

    def process_update_data(self, password=None, salt=None, created=None, id=None, **data):
        return data

    async def _get_user_and_permissions(self, id, columns='*'):
        user, _permissions = await asyncio.gather(
            self.get(id, columns=columns),
            self.get_user_permissions(id))
        return {
            **user,
            'permissions': _permissions['permissions']
        }
