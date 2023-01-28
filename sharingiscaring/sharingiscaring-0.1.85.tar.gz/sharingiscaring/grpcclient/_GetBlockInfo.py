from __future__ import annotations
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient._SharedConverters import Mixin as _SharedConverters
# from sharingiscaring.GRPCClient import GRPCClient
import os
import sys
sys.path.append(os.path.dirname('sharingiscaring'))
from sharingiscaring.GRPCClient.ConcordiumTypes import CCD_BlockInfo
from sharingiscaring.GRPCClient.concordium.v2 import BlockInfo as BP_BlockInfo




class Mixin(_SharedConverters):
    def get_block_info(self,block_hash: str) -> CCD_BlockInfo:
        self.stub:QueriesStub
        prefix = 'block_'
        result = {}
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        
        grpc_return_value:BlockInfo   = self.stub.GetBlockInfo(request=blockHashInput)
        # bi = BP_BlockInfo()
        # bi.parse(grpc_return_value)
        for descriptor in grpc_return_value.DESCRIPTOR.fields:
            key, value = self.get_key_value_from_descriptor(descriptor, grpc_return_value)
            
            if type(value) in self.simple_types:
                result[f"{prefix}{key}"] = self.convertSingleValue(value)
        
        return CCD_BlockInfo(**result)