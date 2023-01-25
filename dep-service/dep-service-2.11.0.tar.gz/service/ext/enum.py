"""Service builtin enums."""

from __future__ import annotations

from typing import List
from enum import Enum


class AclType(str, Enum):
    """Acl type."""

    read = 'r'
    write = 'w'
    exec = 'e'
    admin = 'a'

    @classmethod
    def as_executor(cls) -> List[AclType]:
        """As executor."""
        return [AclType.exec]

    @classmethod
    def as_read_only(cls) -> List[AclType]:
        """Read only acl."""
        return [AclType.read]

    @classmethod
    def as_admin(cls) -> List[AclType]:
        """Admin access acl."""
        return [AclType.read, AclType.write, AclType.exec, AclType.admin]


class SourceType(str, Enum):
    """Lookup source type."""

    market = 'market'
    landings = 'landings'
