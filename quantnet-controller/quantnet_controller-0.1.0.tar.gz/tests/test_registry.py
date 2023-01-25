#!/usr/bin/env python3

import logging
import unittest
import asyncio

from quantnet_controller.mq.registry import Registry

STOP = asyncio.Event()

def handle_register(online, tokens, queue, modules):
    print(online)
    print(tokens)
    print(queue)
    print(modules)
    STOP.set()
    
class TestRegistry(unittest.IsolatedAsyncioTestCase):
    logger = logging.getLogger(__name__)
    log_format = \
        '%(asctime)s - %(name)s - {%(filename)s:%(lineno)d} - [%(threadName)s] - %(levelname)s - %(message)s'
    logging.basicConfig(handlers=[logging.StreamHandler()], format=log_format, force=True)

    async def test_registery(self):
        qns_register = Registry('register_instance_id')      
        await qns_register.start_mqttclient('localhost')
        qns_register.on_register=handle_register
        
        """wait for exit"""
        await STOP.wait()
