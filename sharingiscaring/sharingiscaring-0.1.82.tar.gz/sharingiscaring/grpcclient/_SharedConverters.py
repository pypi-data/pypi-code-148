
from __future__ import annotations
from typing import Protocol
from types_pb2 import *
import base58
import base64
import datetime as dt
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
# from google.protobuf import message

class OpenStatusEnum(Enum):
    openForAll = 0
    closedForNew = 1
    closedForAll = 2

class Mixin(Protocol):
    simple_types = [
            AccountAddress, 
            AbsoluteBlockHeight,
            Amount, 
            AccountThreshold,
            AccountIndex, 
            BakerId, 
            BakerElectionVerifyKey,
            BakerSignatureVerifyKey,
            BakerAggregationVerifyKey,
            BlockHash, 
            BlockHeight,
            Energy,
            GenesisIndex,
            ModuleRef,
            SequenceNumber, 
            Slot,
            StateHash,
            TransactionHash, 
            Timestamp,
            str, int, bool, float]

    def get_key_value_from_descriptor(self, descriptor, the_list):
        return descriptor.name, getattr(the_list, descriptor.name)

    def generate_account_identifier_input_from(self, hex_address:str):
        bin_value       = base58.b58decode_check(hex_address)[1:]
        address         = AccountAddress(value=bin_value)
        account         = AccountIdentifierInput(address=address)
        return account

    def generate_block_hash_input_from(self, hex_block_hash: str):
        return BlockHashInput(given=BlockHash(value=bytes.fromhex(hex_block_hash)))

    def convertHash(self, value):
        return base64.b64decode(MessageToDict(value)['value']).hex()

    def convertSingleValue(self, value):
        if type(value) in [
            BlockHash, 
            TransactionHash, 
            StateHash, 
            ModuleRef,
            BakerElectionVerifyKey,
            BakerSignatureVerifyKey,
            BakerAggregationVerifyKey
            ]:
            return self.convertHash(value)
        elif type(value) == AccountAddress:
            return self.convertAccountAddress(value)
        elif type(value) == Timestamp:
            if 'value' in MessageToDict(value):
                return dt.datetime.fromtimestamp(int(MessageToDict(value)['value']) / 1_000)
            else:
                return {}
        elif type(value) in [
            AbsoluteBlockHeight, 
            Amount, 
            AccountThreshold, 
            AccountIndex,
            BakerId, 
            BakerElectionVerifyKey,
            BakerSignatureVerifyKey,
            BakerAggregationVerifyKey,
            BlockHeight,
            Energy,
            GenesisIndex,
            SequenceNumber, 
            Slot,
            ]:
            return value.value
        elif type(value) in [int, bool, str, float]:
            return value
   
    def convertAccountAddress(self, value: AccountAddress):
        return base58.b58encode_check(b'\x01' + value.value).decode()

    def convertAmount(self, value: Amount):
        return value.value
    
    def convertCommissionRates(self, value):
        result = {}
        for descriptor in value.DESCRIPTOR.fields:
            key, val = self.get_key_value_from_descriptor(descriptor, value)
            result[key] = val.parts_per_hundred_thousand / 100_000
        return result

    def convertBakerPoolInfo(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            
            if type(value) in [BakerId, AccountAddress, Amount, str, int, bool, float]:
                result[key] = self.convertSingleValue(value)

            if type(value) == OpenStatus:
                result[key] = OpenStatusEnum(value).name

            elif type(value) == CommissionRates:
                result[key] = self.convertCommissionRates(value)

        return result

    def convertPoolCurrentPaydayInfo(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            result[key] = self.convertSingleValue(value)

        return result

    def converPendingChange_Reduce_Remove(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            result[key] = self.convertSingleValue(value)

        return result

    def converPendingChange(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
           
            if message.WhichOneof("change") == "reduce" and key == 'reduce':
                result[key] = self.converPendingChange_Reduce_Remove(value)
            elif message.WhichOneof("change") == "remove" and key == 'remove':
                result[key] = self.converPendingChange_Reduce_Remove(value)

        return result

