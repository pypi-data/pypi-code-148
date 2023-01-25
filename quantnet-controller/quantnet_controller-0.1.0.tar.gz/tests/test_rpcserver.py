#!/usr/bin/env python3

import logging
import unittest
import asyncio

from quantnet_controller.mq.rpcserver import RPCServer

STOP = asyncio.Event()

def handle_rpcmsg(server, body, props):
    print(body['cmd'])
    print(body['params'])
    res['code'] = 101
    res['error'] = 'unknown command'
    server.send_response(res. props)
    
class TestRPCServer(unittest.IsolatedAsyncioTestCase):
    logger = logging.getLogger(__name__)
    log_format = \
        '%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - [%(threadName)s] - %(levelname)s - %(message)s'
    logging.basicConfig(handlers=[logging.StreamHandler()], format=log_format, force=True)

    async def test_server(self):
        rpcserver = RPCServer('server_id')      
        rpcserver.on_rpcmsg = handle_rpcmsg
        await rpcserver.start_mqttclient('localhost')
        
        """ wait for exit """
        await STOP.wait()
