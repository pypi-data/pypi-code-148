from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from enum import Enum
from sharingiscaring.GRPCClient._SharedConverters import Mixin as _SharedConverters
from google.protobuf.json_format import MessageToJson, MessageToDict
import os
import sys
sys.path.append(os.path.dirname('sharingiscaring'))
# from sharingiscaring.block import ConcordiumBlockInfo
from sharingiscaring.GRPCClient.ConcordiumTypes import CCD_TokenomicsInfo
import math


class Mixin(_SharedConverters):
    def convertTokenomicsV0(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if type(value) in self.simple_types:
                        result[key] = self.convertSingleValue(value)
                    elif type(value) == ProtocolVersion:
                        result[key] = value
                    
            return result

    def convertTokenomicsV1(self, message):
        if MessageToDict(message) == {}:
            return None
        else:
            result = {}
            for descriptor in message.DESCRIPTOR.fields:
                    key, value = self.get_key_value_from_descriptor(descriptor, message)
                    if type(value) in self.simple_types:
                        result[key] = self.convertSingleValue(value)
                    elif type(value) == ProtocolVersion:
                        result[key] = value
                    elif type(value) == MintRate:
                        result[key] = value.mantissa * math.pow(10, -1*value.exponent)
                    
            return result


    def get_tokenomics_info(self,block_hash: str) -> CCD_TokenomicsInfo:
        self.stub:QueriesStub
        prefix = ''
        result = {}
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:BlockInfo   = self.stub.GetTokenomicsInfo(request=blockHashInput)
        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, grpc_return_value)
            
            if type(value) == TokenomicsInfo.V0:
                result[f"{prefix}{key}"] = self.convertTokenomicsV0(value)
            elif type(value) == TokenomicsInfo.V1:
                result[f"{prefix}{key}"] = self.convertTokenomicsV1(value)
        
        return CCD_TokenomicsInfo(**result)