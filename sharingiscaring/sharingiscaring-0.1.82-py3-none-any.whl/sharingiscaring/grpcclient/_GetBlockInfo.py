from __future__ import annotations
from service_pb2_grpc import QueriesStub
from types_pb2 import *
from enum import Enum
from _SharedConverters import Mixin as _SharedConverters
import os
import sys
sys.path.append(os.path.dirname('sharingiscaring'))
# from sharingiscaring.block import ConcordiumBlockInfo
from ConcordiumTypes.types import CCD_BlockInfo




class Mixin(_SharedConverters):
    def get_block_info(self,block_hash: str) -> CCD_BlockInfo:
        self.stub:QueriesStub
        prefix = 'block_'
        result = {}
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:BlockInfo   = self.stub.GetBlockInfo(request=blockHashInput)
        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, grpc_return_value)
            
            if type(value) in self.simple_types:
                result[f"{prefix}{key}"] = self.convertSingleValue(value)
        
        return CCD_BlockInfo(**result)