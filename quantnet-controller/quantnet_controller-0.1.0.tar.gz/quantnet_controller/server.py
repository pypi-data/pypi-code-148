"""
Main module.
"""
import asyncio
import os
import signal
import time
import argparse
import logging

import uvloop
# from distutils.command.config import config
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

from types import FrameType
from typing import TYPE_CHECKING, List, Optional, Sequence, Set, Tuple, Union

from quantnet_controller.mq.rpcserver import RPCServer
from quantnet_controller.mq.rpcclient import RPCClient
from quantnet_controller.mq.registry import Registry
from quantnet_controller.mq.gmqtt.mqttclient import MQTTClient
from quantnet_controller.common.config import Config

logger = logging.getLogger("quantnet.error")

def handle_register(online, tokens, queue, modules):
    print(online)
    print(tokens)
    print(queue)
    print(modules)
    
def handle_rpcmsg(server, body, props):
    print(body['cmd'])
    print(body['params'])
    res['code'] = 101
    res['error'] = 'unknown command'
    server.send_response(res. props)
    
class QuantnetServer:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.started = False
        self.should_exit = False
        self.force_exit = False
        self.server_registry = None
        
    def run(self) -> None:
        # self.config.setup_event_loop()
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        return asyncio.run(self.serve())

    async def serve(self) -> None:
        process_id = os.getpid()
        
        config = self.config
        # if not config.loaded:
        #     config.load()
            
        """ install signal handlers """
        loop = asyncio.get_event_loop()
        try:
            loop.add_signal_handler(signal.SIGINT, self.handle_exit, signal.SIGINT, None)
            loop.add_signal_handler(signal.SIGTERM, self.handle_exit, signal.SIGTERM, None)
        except NotImplementedError:
            return
        
        message = "Started server process [%d]"
        logger.info(message, process_id)
        
        await self.startup()
        if self.should_exit:
            return
        await self.main_loop()
        await self.shutdown()
        
        message = "Finished server process [%d]"
        logger.info(message, process_id)
        
    async def startup(self) -> None:
        config = self.config
        
        loop = asyncio.get_running_loop()
    
        self.server_registry = server_registry = Registry('quantnet_server_registry')
        server_registry.on_register = handle_register
        await server_registry.start()
        
        self.rpcserver = rpcserver = RPCServer('server_id')      
        rpcserver.on_rpcmsg = handle_rpcmsg
        await rpcserver.start()
        
        self.started = True

    async def main_loop(self) -> None:
        counter = 0
        should_exit = self.should_exit
        while not should_exit:
            counter += 1
            counter = counter % 864000
            await asyncio.sleep(0.1)
            should_exit = self.should_exit

    async def shutdown(self) -> None:
        logger.info("Shutting down")
        
        await self.rpcserver.stop()
        await self.server_registry.stop()
        
        
    def handle_exit(self, sig: int, frame: Optional[FrameType]) -> None:
        if self.should_exit and sig == signal.SIGINT:
            self.force_exit = True
        else:
            self.should_exit = True
        
        
            