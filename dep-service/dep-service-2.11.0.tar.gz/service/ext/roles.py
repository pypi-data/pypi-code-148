"""Service builtin roles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from logging import getLogger

from jwt import encode as jwt_encode, decode as jwt_decode

from service.ext.enum import AclType

log = getLogger(__name__)
jwt_algorithm = 'HS256'


@dataclass(frozen=True)
class Role:
    """Roles."""

    name: str
    acl: List[AclType]

    @staticmethod
    def read(token: str, secret: str) -> Optional[Role]:
        """Decode service token to a role."""
        try:
            obj = jwt_decode(token, secret, algorithms=[jwt_algorithm])
            return Role(
                name=obj.get('name'),
                acl=[AclType(p) for p in obj.get('acl')],
            )
        except Exception as _fault_read:  # noqa
            log.error(f'Read role: {_fault_read}')
            return

    def token(self, secret: str) -> str:
        """Role token."""

        payload = {
            'name': self.name,
            'acl': ''.join([perm.value for perm in self.acl]),
        }

        return jwt_encode(payload, secret, algorithm=jwt_algorithm)

    def is_admin(self) -> bool:
        """Is admin."""
        return any([acl == AclType.admin for acl in self.acl])

    def can_execute(self) -> bool:
        """Can execute."""
        return any([acl in (AclType.admin, AclType.exec) for acl in self.acl])

    def can_write(self) -> bool:
        """Can write."""
        return any([acl in (AclType.admin, AclType.write) for acl in self.acl])


role_read = Role(name='read', acl=AclType.as_read_only())
role_exec = Role(name='exec', acl=AclType.as_executor())
role_admin = Role(name='admin', acl=AclType.as_admin())
