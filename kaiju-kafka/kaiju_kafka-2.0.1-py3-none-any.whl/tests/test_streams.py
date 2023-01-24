import asyncio

import aiokafka
from kaiju_tools.streams.tests.test_streams import stream_test_function

from .fixtures import *


@pytest.mark.asyncio
@pytest.mark.docker
async def test_kafka_listener(kafka, redis, kafka_listener, logger):

    c = aiokafka.AIOKafkaConsumer(
        loop=asyncio.get_running_loop(),
        **{
            'bootstrap_servers': '0.0.0.0:9092',
            'group_id': 'pytest',
            'auto_offset_reset': 'earliest',
            'enable_auto_commit': False,
        },
    )
    await c.start()
    c.subscribe(['dev-pytest-pytest-rpc', 'dev-pytest-pytest-callback'])
    await c.getmany(timeout_ms=50)
    await c.stop()

    await asyncio.sleep(5)

    await stream_test_function(kafka_listener, logger)
