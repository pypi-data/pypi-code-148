from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
import base58
import base64
import datetime as dt
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf import message
from sharingiscaring.GRPCClient._SharedConverters import Mixin as _SharedConverters
import os
import sys
sys.path.append(os.path.dirname('sharingiscaring'))
from sharingiscaring.GRPCClient.ConcordiumTypes import CCD_AccountInfo, CCD_AccountStakingInfo
from sharingiscaring.GRPCClient.concordium.v2 import AccountInfo


class Mixin(_SharedConverters):
    def convertCredentials(self,message):
        cred_list = []
        for key in message.keys():
            dd = {}
            cred_list.append(MessageToDict(message[key]))
        return cred_list
    
    def convertList(self, message):
        entries = []

        for list_entry in message:
            entries.append(self.convertSingleValue(list_entry))
            
        return entries

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

    def convertBakerInfo(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                
                if type(value) in self.simple_types:
                    result[key] = self.convertSingleValue(value)
                
        return result

    def convertDelegationTarget(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, message)
                
                if type(value) == Empty:
                    pass
                if type(value) == BakerId:
                    if MessageToDict(value) == {}:
                        result['passive'] = 'passiveDelegation'
                    else:
                        result['baker_id'] = self.convertSingleValue(value)
                
        return result


    def convertAccountStakingInfo(self, message: message):
        result = {}
        which_one = message.WhichOneof("staking_info")
        if not which_one:
            return None
        else:
            if which_one == "baker":
                for descriptor in getattr(message, which_one).DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, getattr(message, which_one))
                    if type(value) in [BakerId, AccountAddress, Amount, str, int, bool, float]:
                        result[key] = self.convertSingleValue(value)
                    
                    elif type(value) == BakerPoolInfo:
                        result[key] = self.convertBakerPoolInfo(value)

                    elif type(value) == BakerInfo:
                        result[key] = self.convertBakerInfo(value)

                    elif type(value) == StakePendingChange:
                        result[key] = self.converPendingChange(value)

            elif which_one == "delegator":
                for descriptor in getattr(message, which_one).DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, getattr(message, which_one))
                    if type(value) in [BakerId, AccountAddress, Amount, str, int, bool, float]:
                        result[key] = self.convertSingleValue(value)
                    
                    elif type(value) == DelegationTarget:
                        result[key] = self.convertDelegationTarget(value)

                    
                    elif type(value) == StakePendingChange:
                        result[key] = self.converPendingChange(value)
            
            return CCD_AccountStakingInfo(**{which_one: result})

    def get_account_info(self, hex_address:str, block_hash: str) -> CCD_AccountInfo:
        self.stub:QueriesStub
        prefix="account_"
        blockHashInput          = self.generate_block_hash_input_from(block_hash)
        accountIdentifierInput  = self.generate_account_identifier_input_from(hex_address)
        account_info            = AccountInfoRequest(
                                    block_hash=blockHashInput, 
                                    account_identifier=accountIdentifierInput)
        
        grpc_return_value = self.stub.GetAccountInfo(request=account_info)
        # ai = AccountInfo(grpc_return_value)
        result = {}
        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, grpc_return_value)
            key_to_store = f"{prefix}{key}"
            if type(value) in self.simple_types:
                result[key_to_store] = self.convertSingleValue(value)
            
            elif type(value) == ReleaseSchedule:
                result[key_to_store] = self.convertRelease(value)

            elif key == 'creds':
                result[f"{prefix}credentials"] = self.convertCredentials(value)

            elif type(value) == AccountStakingInfo:
                result[key_to_store] = self.convertAccountStakingInfo(value)
        
        return CCD_AccountInfo(**result)