from __future__ import annotations
from service_pb2_grpc import QueriesStub
from types_pb2 import *
import grpc
import base58
import base64
import datetime as dt
from rich.progress import track
from rich import print
from enum import Enum
from google.protobuf.json_format import MessageToJson, MessageToDict
from google.protobuf import message
import sys
import os



from _GetPoolInfo import Mixin as _GetPoolInfo
from _GetPoolDelegatorsRewardPeriod import Mixin as _GetPoolDelegatorsRewardPeriod
from _GetAccountInfo import Mixin as _GetAccountInfo
from _GetBlockInfo import Mixin as _GetBlockInfo
from _GetTokenomicsInfo import Mixin as _GetTokenomicsInfo



class GRPCClient(
    _GetPoolInfo,
    _GetPoolDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetTokenomicsInfo
    ):
    
    def __init__(self, host: str='localhost', port: int=20000):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = QueriesStub(self.channel)
        
    
# grpcclient = GRPCClient()
# deleg = grpcclient.get_delegators_for_pool(72723, "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (deleg)

# pool_info = grpcclient.get_pool_info_for_pool(85223, "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# print (pool_info)

#76670
# account_info = grpcclient.get_account_info("4qL7HmpqdKpYufCV7EvL1WnHVowy1CrTQS7jfYgef5stzpftwS", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
#72723
# account_info = grpcclient.get_account_info("3BFChzvx3783jGUKgHVCanFVxyDAn5xT3Y5NL5FKydVMuBa7Bm", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
#delegator
# account_info = grpcclient.get_account_info("4TVoQQ8VRfqjQkG34dXR8NEPHFxQtWyE6ND62YXckJadGxBQsg", 
#                 "affea3382993132bf8fd4f6b5c8548e015ca5b99b074a4f2df57d4878cfce829")
# #passive Delegator
# account_info = grpcclient.get_account_info("3rfJwWcM5AcdpchhXtQ1Zo5aVFjjPpM1DqNT2ucJRLZgu95R7s", 
#                 "af7c0abae81577a9a52621ecfb794a01f1fbb370fe714659f0760644065bdcbd")
# print (account_info)

# # blockInfo
# block_info = grpcclient.get_block_info(
                # "af7c0abae81577a9a52621ecfb794a01f1fbb370fe714659f0760644065bdcbd")
# print (block_info)


# tokenomicsInfo
# tok_info = grpcclient.get_tokenomics_info(
#                 "af7c0abae81577a9a52621ecfb794a01f1fbb370fe714659f0760644065bdcbd")
# print (tok_info)

