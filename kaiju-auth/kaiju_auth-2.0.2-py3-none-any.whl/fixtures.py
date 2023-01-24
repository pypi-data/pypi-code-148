from typing import Union

from kaiju_tools.fixtures import BaseFixtureService
from kaiju_tools.serialization import loads

from .users import *

__all__ = ('UserFixtureService',)


class UserFixtureService(BaseFixtureService):

    group_service_class = GroupService
    permission_service_class = PermissionService
    user_service_class = UserService
    users_subdir = 'users'

    def __init__(
            self,
            permission_service=None,
            group_service=None,
            user_service=None,
            app=None,
            base_dir=BaseFixtureService.BASE_DIR,
            logger=None
    ):
        BaseFixtureService.__init__(self, app=app, base_dir=base_dir, logger=logger)
        self._permission_service: PermissionService = permission_service
        self._group_service: GroupService = group_service
        self._user_service: UserService = user_service

    async def init(self):
        self._permission_service = self.discover_service(name=self._permission_service, cls=self.permission_service_class)
        self._group_service: GroupService = self.discover_service(name=self._group_service, cls=self.group_service_class)
        self._user_service: UserService = self.discover_service(name=self._user_service, cls=self.user_service_class)
        await self.load_user_permissions()
        await self.load_user_groups()
        await self.load_users()

    async def load_user_permissions(self):
        service = self._permission_service
        path = self._base_dir / self.users_subdir / 'permissions.json'
        self.logger.debug('Loading user permissions from: %s.', path)
        data = self.load_file(path)
        if data:
            keys = [row['id'] for row in data]
            existing = await service.m_get(keys, columns='id')
            existing = set(row['id'] for row in existing)
            data = [row for row in data if row['id'] not in existing]
            self.logger.debug('Adding %d new permissions.', len(data))
            if data:
                await service.create(data, columns=None)
        else:
            self.logger.debug('No user permission fixtures have been found.')

    async def load_user_groups(self):
        service = self._group_service
        path = self._base_dir / self.users_subdir / 'groups.json'
        self.logger.debug('Loading user groups from: %s.', path)
        data = self.load_file(path)
        if data:
            for row in data:
                group = row['data']
                _id = group['id']
                group_permissions = row['permissions']
                if not await service.exists(_id):
                    self.logger.debug('Adding new group "%s".', _id)
                    await service.create(group, columns=None)
                if group_permissions:
                    await service.set_permissions(_id, group_permissions)
        else:
            self.logger.debug('No user group fixtures have been found.')

    async def load_users(self):
        service = self._user_service
        path = self._base_dir / self.users_subdir / 'users.json'
        self.logger.debug('Loading users from: %s.', path)
        data = self.load_file(path)
        if data:
            for row in data:
                user = row['data']
                user_groups = row['groups']
                username = user['username']
                data = await service.list(conditions={'username': username}, columns='id')
                data = data['data']
                if data:
                    user_id = data[0]['id']
                else:
                    self.logger.debug('Adding new user "%s".', username)
                    user = await service.register(**user)
                    user_id = user['id']
                if user_groups:
                    await service.set_user_groups(user_id, user_groups)
        else:
            self.logger.debug('No user fixtures have been found.')
