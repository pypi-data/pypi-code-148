from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *
from sharingiscaring.GRPCClient.service_pb2_grpc import QueriesStub
import base58
import base64
import datetime as dt
from google.protobuf.json_format import MessageToJson, MessageToDict
from sharingiscaring.GRPCClient._SharedConverters import Mixin as _SharedConverters
from typing import Callable, Iterator, Union, Optional
from sharingiscaring.GRPCClient.ConcordiumTypes import CCD_DelegatorInfo

class Mixin(_SharedConverters):
    def get_delegators_for_pool(self, pool_id:int, block_hash: str):
        self.stub: QueriesStub
        result = []
        blockHashInput      = self.generate_block_hash_input_from(block_hash)
        baker_id            = BakerId(value=pool_id)
        delegatorsRequest   = GetPoolDelegatorsRequest(
                                    baker=baker_id, 
                                    block_hash=blockHashInput)
        
        grpc_return_value:Iterator[DelegatorRewardPeriodInfo] = \
            self.stub.GetPoolDelegatorsRewardPeriod(request=delegatorsRequest)
        
        for delegator in list(grpc_return_value):
            
            result.append( CCD_DelegatorInfo(**{
                'account': self.convertAccountAddress(delegator.account),
                'stake':   self.convertAmount(delegator.stake)
            } ))

        return result