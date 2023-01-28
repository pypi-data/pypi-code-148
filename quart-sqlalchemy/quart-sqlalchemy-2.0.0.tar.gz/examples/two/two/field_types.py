from typing import Any

import boto3
from mypy_boto3_kms.client import KMSClient
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConstrainedStr
from pydantic import SecretStr

from two.crypto_util import decrypt
from two.crypto_util import encrypt
from two.crypto_util import get_kms_client


key_id = "91d9a9c8-0651-4ded-8c93-e5ed9e06d8f1"
kms = boto3.client("kms")


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        validate_all = True
        orm_mode = True
        use_enum_values = True

    @classmethod
    def _get_value(cls, v: Any, *args: Any, **kwargs: Any) -> Any:
        """Hack to enable smarter serialization behavior.

        This wrapper will check for a `__serialize__` instance method defined on the custom field
        class and use that for serialization if it exists.  Then it will check the type against
        the json_encoders defined in the model config and use the first one that matches.  Failing
        that, it will fallback to default behvior.

        By doing this before rather than after, we can even ensure correct serialization
        of custom field types that inherit from python scalars such as str, int, etc.

        This work is inspired by: https://github.com/pydantic/pydantic/issues/951
        """
        if hasattr(v, "__serialize__"):
            return v.__serialize__()
        for type_, converter in cls.__config__.json_encoders.items():
            if isinstance(v, type_):
                return converter(v)

        return super()._get_value(v, *args, **kwargs)


class EncryptedSecret(ConstrainedStr):
    @classmethod
    def validate(cls, value, config):
        key_id, kms = cls._get_kms_args(config)
        decrypted = decrypt(key_id, value, kms)
        return ConstrainedStr(decrypted)

    @classmethod
    def _get_kms_args(cls, config):
        key_id = getattr(config, "kms_key_id", None)
        kms = getattr(config, "kms_client", None)
        if key_id is None or kms is None:
            raise ValueError(
                f"kms_key_id and kms_client must be set in Config to use {cls.__name__}"
            )
        if callable(kms):
            kms = kms()
        return key_id, kms

    def encrypt(self, key_id: str, kms: KMSClient):
        value = encrypt(key_id, self, kms)
        return EncryptedSecret(value)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(  # pragma: no cover
            examples=["jNkGJXh4LTcIfkWfUpatlUpEWXfJvU71"],
        )


# class Example(BaseModel):
#     class Config:
#         kms_key_id = "some_key"
#         kms_client = get_kms_client()

#     secret: EncryptedSecret = EncryptedSecret(
#         "AQICAHi4b5SNvuUHTVjg/flY91hbzyWOMWLx7tvWqwyLKT1V2gF738bj8MEr0Oea7WYMBELnAAAAZDBiBgkqhkiG9w0BBwagVTBTAgEAME4GCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMtmdJmtU8GSChFKmFAgEQgCFSDhugVHHiywNaFUfhb7odnsdMjxKH2BwO5EwDnDCJG/Y="
#     )
