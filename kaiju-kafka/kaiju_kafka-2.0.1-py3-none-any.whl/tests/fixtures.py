from time import sleep

import pytest

from kaiju_tools.streams.etc import Topics
from kaiju_tools.docker import DockerContainer
from kaiju_tools.tests.fixtures import *
from kaiju_redis.tests.fixtures import *

from ..services import *


KAFKA_HOST = '0.0.0.0'
ZK_PORT = '2181'
KAFKA_PORT = '9092'
TEST_TOPIC = str(uuid.uuid4())


def _kafka_container(logger):
    return DockerContainer(
        image='johnnypark/kafka-zookeeper',
        name='pytest-kafka',
        version='latest',
        ports={'9092': str(KAFKA_PORT), '2181': str(ZK_PORT)},
        env={'ADVERTISED_HOST': KAFKA_HOST, 'ADVERTISED_PORT': KAFKA_PORT},
        sleep_interval=2.0,
        remove_on_exit=True,
        logger=logger
        # healthcheck={
        #     'test': "/opt/kafka_2.12-2.*/bin/kafka-topics.sh --list --zookeeper=localhost:2181",
        #     'interval': 100000000,
        #     'timeout': 6000000000,
        #     'start_period': 5000000000,
        #     'retries': 3
        # }
    )


@pytest.fixture
def kafka(logger):
    """Return a new kafka/zk container. See `kaiju_tools.tests.fixtures.container` for more info."""
    with _kafka_container(logger) as c:
        sleep(10)
        yield c


@pytest.fixture(scope='session')
def per_session_kafka(logger):
    """Return a new kafka container. See `kaiju_tools.tests.fixtures.per_session_container` for more info."""
    with _kafka_container(logger) as c:
        sleep(10)
        yield c


@pytest.fixture
def kafka_listener(redis_transport, redis_locks, rpc_interface, logger):
    return KafkaListener(
        app=redis_transport.app,
        topics=[Topics.rpc, Topics.callback],
        rpc_service=rpc_interface,
        locks_service=redis_locks,
        consumer_settings={
            'bootstrap_servers': f'0.0.0.0:{KAFKA_PORT}',
            'timeout_ms': 1000,
            'group_id': 'pytest',
            'auto_offset_reset': 'earliest',
            'enable_auto_commit': False,
        },
        producer_settings={'bootstrap_servers': f'0.0.0.0:{KAFKA_PORT}'},
        logger=logger,
    )
