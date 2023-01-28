from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient._SharedConverters import Mixin as _SharedConverters
# from sharingiscaring.GRPCClient import GRPCClient
import os
import sys
sys.path.append(os.path.dirname('sharingiscaring'))
from sharingiscaring.GRPCClient.ConcordiumTypes import *
from google.protobuf.json_format import MessageToJson, MessageToDict





class Mixin(_SharedConverters):
    def convertNewRelease(self, message):
        schedule = []
        for entry in message:
            entry_dict = {}
            for descriptor in entry.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if type(value) in self.simple_types:
                    converted_value = self.convertSingleValue(value)        
                    if converted_value:
                        entry_dict[key] = converted_value
            schedule.append(CCD_NewRelease(**entry_dict))
        
        return schedule

    def convertEvents(self, message):
        events = []
        for entry in message:
            entry_dict = {}
            for descriptor in entry.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if type(value) in self.simple_types:
                    converted_value = self.convertSingleValue(value)        
                    if converted_value:
                        entry_dict[key] = converted_value
            if entry_dict == {}:
                    pass
            else:
                events.append(entry_dict)
        
        return events

    def convertInstanceInterruptedEvent(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        
                
            if key == 'events':
                        result[key] = self.convertEvents(value)

        return CCD_ContractTraceElement_Interrupted(**result)

    def convertInstanceUpdatedEvent(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        
                
            if key == 'events':
                        result[key] = self.convertEvents(value)

        return CCD_InstanceUpdatedEvent(**result)

    def convertInstanceResumedEvent(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

        return CCD_ContractTraceElement_Resumed(**result)

    def convertInstanceTransferredEvent(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

        return CCD_ContractTraceElement_Transferred(**result)

    def convertUpdateEvents(self, message):
        events = []
        for entry in message:
            
            for descriptor in entry.DESCRIPTOR.fields:
                entry_dict = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if MessageToDict(value) == {}:
                        pass
                else:
                    if type(value) == InstanceUpdatedEvent:
                        entry_dict[key] = self.convertInstanceUpdatedEvent(value)
                    
                    if type(value) == ContractTraceElement.Interrupted:
                        entry_dict[key] = self.convertInstanceInterruptedEvent(value)

                    if type(value) == ContractTraceElement.Resumed:
                        entry_dict[key] = self.convertInstanceResumedEvent(value)

                    if type(value) == ContractTraceElement.Transferred:
                        entry_dict[key] = self.convertInstanceTransferredEvent(value)

                    if type(value) in self.simple_types:
                        converted_value = self.convertSingleValue(value)        
                        if converted_value:
                            entry_dict[key] = converted_value
                if entry_dict == {}:
                    pass
                else:
                    events.append(entry_dict)
        
        return events

    def convertBakerKeysEvent(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

        return CCD_BakerKeysEvent(**result)

    def convertEffectBakerAdded(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

            if type(value) == BakerKeysEvent:
                result[key] = self.convertBakerKeysEvent(value)        

        return CCD_BakerAdded(**result)

    def convertBakerStakeUpdatedData(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

        return CCD_BakerStakeUpdatedData(**result)

    def convertEffectBakerStakeUpdated(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

            if type(value) == BakerStakeUpdatedData:
                result[key] = self.convertBakerStakeUpdatedData(value)        

        return CCD_BakerStakeUpdated(**result)

    def convertBakerStakeIncreased(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if type(value) in self.simple_types:
                result[key] = self.convertSingleValue(value)        

        return CCD_BakerStakeIncreased(**result)

    def convertBakerConfiguredEvents(self, message):
        events = []
        for entry in message:
            
            for descriptor in entry.DESCRIPTOR.fields:
                result = {}
                key, value = self.get_key_value_from_descriptor(descriptor, entry)
                if MessageToDict(value) == {}:
                        pass
                else:
                    if type(value) == BakerEvent.BakerStakeIncreased:
                        result[key] = self.convertBakerStakeIncreased(value)
                        events.append(result)
                        
        return events 


    def convertEffectBakerConfigured(self, message):
        result = {}
        for descriptor in message.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, message)
            if key == 'events':
                result[key] = self.convertBakerConfiguredEvents(value)       

        return CCD_BakerConfigured(**result)

    def convertEffectAccountTransfer(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if MessageToDict(value) == {}:
                        pass
                    else:
                        if type(value) in self.simple_types:
                            result[key] = self.convertSingleValue(value)
                    
            return CCD_AccountTransfer(**result)

    def convertEffectAccountTransferWithSchedule(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if key == 'amount':
                        result[key] = self.convertNewRelease(value)
                    
                    elif type(value) in self.simple_types:
                            converted_value = self.convertSingleValue(value)        
                            if converted_value:
                                result[key] = converted_value
                    
            return CCD_TransferredWithSchedule(**result)
        
    def convertEffectContractInitializedEvent(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if key == 'events':
                        result[key] = self.convertEvents(value)
                    
                    elif type(value) in self.simple_types:
                            converted_value = self.convertSingleValue(value)        
                            if converted_value:
                                result[key] = converted_value
                    
            return result

    def convertEffectContractUpdateIssued(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if key == 'effects':
                        result[key] = self.convertUpdateEvents(value)
                    
            return CCD_ContractUpdateIssued(**result)

    def convertAccountTransactionEffects(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    # key ='effect'
                    if MessageToDict(value) == {}:
                        pass
                    else:
                        try:
                            reject_reason = value.reject_reason
                            result['outcome'] = 'reject'
                            result[key] = MessageToDict(value, preserving_proto_field_name=True)#['rejectReason']
                        except:
                            result['outcome'] = 'success'
                            if type(value) in self.simple_types:
                                result[key] = self.convertSingleValue(value)

                                
                            if type(value) == AccountTransactionEffects.AccountTransfer:
                                result[key] = self.convertEffectAccountTransfer(value)

                            if type(value) == AccountTransactionEffects.TransferredWithSchedule:
                                result[key] = self.convertEffectAccountTransferWithSchedule(value)
                            
                            if type(value) == ContractInitializedEvent:
                                result[key] = self.convertEffectContractInitializedEvent(value)

                            if type(value) == RegisteredData:
                                result[key] = self.convertSingleValue(value)

                            if type(value) == AccountTransactionEffects.ContractUpdateIssued:
                                result[key] = self.convertEffectContractUpdateIssued(value)

                            if type(value) == BakerEvent.BakerAdded:
                                result[key] = self.convertEffectBakerAdded(value)

                            if type(value) == BakerId:
                                result[key] = self.convertSingleValue(value)

                            if type(value) == AccountTransactionEffects.BakerStakeUpdated:
                                result[key] = self.convertEffectBakerStakeUpdated(value)

                            if type(value) == AccountTransactionEffects.BakerConfigured:
                                result[key] = self.convertEffectBakerConfigured(value)
                                
            return CCD_AccountTransactionEffects(**result)

    def convertAccountTransactionDetails(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if MessageToDict(value) == {}:
                        pass
                    else:   
                        if type(value) in self.simple_types:
                            result[key] = self.convertSingleValue(value)
                        
                        if type(value) == AccountTransactionEffects:
                            result[key] = self.convertAccountTransactionEffects(value)
                        
            return CCD_AccountTransactionDetails(**result)

    def get_block_transaction_events(self,block_hash: str) -> CCD_Block:
        self.stub:QueriesStub
        prefix = ''
        
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value   = self.stub.GetBlockTransactionEvents(request=blockHashInput)
        tx_list = []
        for tx in list(grpc_return_value):
            result = {}
            for descriptor in tx.DESCRIPTOR.fields:
                key, value = self.get_key_value_from_descriptor(descriptor, tx)
        
                if type(value) in self.simple_types:
                    result[f"{prefix}{key}"] = self.convertSingleValue(value)
            
                if type(value) == AccountTransactionDetails:
                    result[f"{prefix}{key}"] = self.convertAccountTransactionDetails(value)
            tx_list.append(CCD_Transaction(**result))
            
        #     if type(value) in self.simple_types:
        #         result[f"{prefix}{key}"] = self.convertSingleValue(value)
        
        return CCD_Block(**{'transaction_summaries': tx_list})