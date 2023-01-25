"""
Credentials file data model
"""
from __future__ import annotations

import os

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Literal

from pydantic import Field, FilePath, NoneStr, SecretStr, root_validator, validator

from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny  # pragma: no cover


class CredentialRequiredService(HopprBaseModel):
    """
    CredentialRequiredServices data model
    """

    url: str
    user_env: NoneStr = None
    username: str = Field(..., alias="user")
    pass_env: str

    @root_validator(pre=True)
    @classmethod
    def validate_credentials(cls, values: DictStrAny) -> DictStrAny:
        """
        Dynamically parse credentials using specified environment variables
        """
        user_env = values.get("user_env")
        if user_env is not None:
            username = os.environ.get(values["user_env"], "")
            assert len(username) > 0
            values["user"] = username

        return values


class CredentialsFile(HopprBaseSchemaModel):
    """
    Credentials file data model
    """

    kind: Literal["Credentials", "credentials"]
    credential_required_services: list[CredentialRequiredService] = Field(
        [],
        unique_items=True,
        description=(
            "List of CredentialRequiredService objects to provide "
            "authentication to remote repositories and/or registries"
        ),
    )


class CredentialRequiredServicePassword(CredentialRequiredService):
    """
    CredentialsSettings data model to parse `pass_env` environment variable value
    """

    password: SecretStr = SecretStr("")

    @validator("password", pre=True, always=True, allow_reuse=True)
    @classmethod
    def validate_password(cls, password: str, values: DictStrAny) -> SecretStr:
        """
        Extract and return list of `pass_env` values from CredentialRequiredService objects
        """
        pass_env = values["pass_env"]
        password = os.environ.get(pass_env, "")
        assert len(password) > 0

        return SecretStr(password)


class CredentialsMap(HopprBaseModel):
    """
    Maps a repository URL to its associated credentials for fast lookup
    """

    __root__: dict[str, CredentialRequiredServicePassword]

    def __getitem__(self, item: str) -> CredentialRequiredServicePassword:
        return self.__root__[item]

    def __setitem__(self, item: str, value: CredentialRequiredServicePassword) -> None:
        self.__root__[item] = value


class Credentials(CredentialsFile):
    """
    CredentialsModel populated with environment variable passwords
    """

    lookup: ClassVar[CredentialsMap] = CredentialsMap(__root__={})

    def __getitem__(self, item: str) -> CredentialRequiredServicePassword:
        return self.lookup[item]

    @validator("credential_required_services", allow_reuse=True)
    @classmethod
    def validate_services(cls, services: list[CredentialRequiredService]) -> list[CredentialRequiredServicePassword]:
        """
        Transform CredentialRequiredService list into CredentialRequiredServicePassword list
        """
        password_services: list[CredentialRequiredServicePassword] = []

        for service in services:
            service_password_obj = CredentialRequiredServicePassword(
                url=service.url, user=service.username, pass_env=service.pass_env  # type: ignore[call-arg]
            )
            cls.lookup[service.url] = service_password_obj
            password_services.append(service_password_obj)

        return password_services

    @classmethod
    def find(cls, url: str) -> CredentialRequiredServicePassword | None:
        """
        Return credentials for a repo URL
        """
        return cls.lookup.__root__.get(url)

    @classmethod
    def load(cls, source: str | FilePath | DictStrAny | None) -> Credentials | None:
        """
        Load credentials file from local path or dict
        """
        if source is None:
            return None

        if isinstance(source, dict):
            return cls.parse_obj(source)

        if isinstance(source, (str, Path)):
            return cls.parse_file(source)

        raise TypeError("'source' argument must be one of: 'str', 'Path', 'dict[str, Any]'")
