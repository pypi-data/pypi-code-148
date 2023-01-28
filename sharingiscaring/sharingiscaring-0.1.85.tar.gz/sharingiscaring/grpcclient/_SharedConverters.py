
from __future__ import annotations
from typing import Protocol
from sharingiscaring.GRPCClient.types_pb2 import *
import base58
import base64
import datetime as dt
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from sharingiscaring.GRPCClient.ConcordiumTypes import *
# from google.protobuf import message

class OpenStatusEnum(Enum):
    openForAll = 0
    closedForNew = 1
    closedForAll = 2

class TransactionType(Enum):
    DEPLOY_MODULE = 0
    INIT_CONTRACT = 1
    UPDATE = 2
    TRANSFER = 3
    ADD_BAKER = 4
    REMOVE_BAKER = 5
    UPDATE_BAKER_STAKE = 6
    UPDATE_BAKER_RESTAKE_EARNINGS = 7
    UPDATE_BAKER_KEYS = 8
    UPDATE_CREDENTIAL_KEYS = 9
    ENCRYPTED_AMOUNT_TRANSFER = 10
    TRANSFER_TO_ENCRYPTED = 11
    TRANSFER_TO_PUBLIC = 12
    TRANSFER_WITH_SCHEDULE = 13
    UPDATE_CREDENTIALS = 14
    REGISTER_DATA = 15
    TRANSFER_WITH_MEMO = 16
    ENCRYPTED_AMOUNT_TRANSFER_WITH_MEMO = 17
    TRANSFER_WITH_SCHEDULE_AND_MEMO = 18
    CONFIGURE_BAKER = 19
    CONFIGURE_DELEGATION = 20

class Mixin(Protocol):
    simple_types = [
            AccountAddress, 
            Address,
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
            BlockItemSummary.TransactionIndex,
            ContractAddress,
            Energy,
            GenesisIndex,
            InitName,
            Memo,
            ModuleRef,
            Parameter,
            ReceiveName,
            RegisteredData,
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
        if MessageToDict(value) == {}:
            return None
        else:
            return base64.b64decode(MessageToDict(value)['value']).hex()

    def convertSingleValue(self, value):
        if type(value) in [
            BlockHash, 
            TransactionHash, 
            StateHash, 
            Memo,
            ModuleRef,
            BakerElectionVerifyKey,
            BakerSignatureVerifyKey,
            BakerAggregationVerifyKey,
            RegisteredData,
            Parameter
            ]:
            return self.convertHash(value)
        elif type(value) == AccountAddress:
            return self.convertAccountAddress(value)
        elif type(value) == Timestamp:
            if 'value' in MessageToDict(value):
                return dt.datetime.fromtimestamp(int(MessageToDict(value)['value']) / 1_000)
            else:
                return {}
        elif type(value) == Address:
            if MessageToDict(value.account) == {}:
                return CCD_Address(**{'contract':  {'index': value.contract.index, 'subindex': value.contract.subindex}}) 
            else:
                return CCD_Address(**{'account': self.convertAccountAddress(value.account)})
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
            BlockItemSummary.TransactionIndex,
            Energy,
            InitName,
            GenesisIndex,
            ReceiveName,
            SequenceNumber, 
            Slot,
            ]:
            return value.value
        elif type(value) == ContractAddress:
            return {'index': value.index, 'subindex': value.subindex}
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

    def convertRelease(self, message):
        resulting_dict = {}
        
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            
            if key == 'schedules':
                schedule = []
                for entry in value:
                    entry_dict = {}
                    for descriptor in entry.DESCRIPTOR.fields:
                        key, value = self.get_key_value_from_descriptor(descriptor, entry)
                        if key == 'transactions':
                            entry_dict[key] = self.convertList(value)
                        elif type(value) == Timestamp:
                            entry_dict[key] = self.convertSingleValue(value)        
                    schedule.append(entry_dict)
                resulting_dict['schedules'] = schedule
            elif type(value) == Amount:
                resulting_dict[key] = self.convertSingleValue(value) 
        return resulting_dict

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

    def convertPendingChange(self, message):
        result = {}

        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
           
            if message.WhichOneof("change") == "reduce" and key == 'reduce':
                result[key] = self.converPendingChange_Reduce_Remove(value)
            elif message.WhichOneof("change") == "remove" and key == 'remove':
                result[key] = self.converPendingChange_Reduce_Remove(value)

        return result

