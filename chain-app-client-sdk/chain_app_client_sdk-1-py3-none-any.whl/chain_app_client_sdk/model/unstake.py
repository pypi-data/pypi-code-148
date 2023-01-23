# coding: utf-8

"""
    Chain App BIND client SDK

    Description for BIND.   # noqa: E501

    The version of the OpenAPI document: 2.0
    Contact: support@bind.com
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from chain_app_client_sdk import schemas  # noqa: F401


class Unstake(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "amount",
            "is_self_staked",
            "is_checking_fee",
        }
        
        class properties:
            amount = schemas.NumberSchema
            is_self_staked = schemas.BoolSchema
            locking_period = schemas.BoolSchema
            __annotations__ = {
                "amount": amount,
                "is_self_staked": is_self_staked,
                "locking_period": locking_period,
            }
    
    amount: MetaOapg.properties.amount
    is_self_staked: MetaOapg.properties.is_self_staked
    is_checking_fee: schemas.AnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_self_staked"]) -> MetaOapg.properties.is_self_staked: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["locking_period"]) -> MetaOapg.properties.locking_period: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "is_self_staked", "locking_period", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_self_staked"]) -> MetaOapg.properties.is_self_staked: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["locking_period"]) -> typing.Union[MetaOapg.properties.locking_period, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "is_self_staked", "locking_period", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, float, ],
        is_self_staked: typing.Union[MetaOapg.properties.is_self_staked, bool, ],
        is_checking_fee: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        locking_period: typing.Union[MetaOapg.properties.locking_period, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Unstake':
        return super().__new__(
            cls,
            *args,
            amount=amount,
            is_self_staked=is_self_staked,
            is_checking_fee=is_checking_fee,
            locking_period=locking_period,
            _configuration=_configuration,
            **kwargs,
        )
