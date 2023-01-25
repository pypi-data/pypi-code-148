#!/usr/bin/env python3

import logging
# import threading
import unittest
# import pytest
# import time
# import uuid
import asyncio

from quantnet_controller.mq.rpcserver import RPCClient

STOP = asyncio.Event()

def handle_rpcmsg(server, body, props):
    print(body['cmd'])
    print(body['params'])
    res['code'] = 101
    res['error'] = 'unknown command'
    server.send_response(res. props)
    
class TestRPCClient(unittest.IsolatedAsyncioTestCase):
    logger = logging.getLogger(__name__)
    log_format = \
        '%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - [%(threadName)s] - %(levelname)s - %(message)s'
    logging.basicConfig(handlers=[logging.StreamHandler()], format=log_format, force=True)

    async def test_server(self):
        rpcclient = RPCClient('client_id')      
        await rpcclient.start_mqttclient('localhost')
        params = {
            'cmd': 'query',
            'param': 'capability'
            }
        response = rpcclient.call('server_id', params)
        print(response)
        
        await STOP.wait()
