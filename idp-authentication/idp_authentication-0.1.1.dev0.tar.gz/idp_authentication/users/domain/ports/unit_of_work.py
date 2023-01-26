from abc import ABC

from idp_authentication.users.domain.ports.repository import (
    UserRepositoryPort,
    UserRoleRepositoryPort,
)
from idp_authentication.users.domain.ports.session import SessionPort


class UnitOfWorkPort(ABC):
    session: SessionPort

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class UsersUnitOfWorkPort(UnitOfWorkPort, ABC):
    user_repository: UserRepositoryPort
    user_role_repository: UserRoleRepositoryPort
