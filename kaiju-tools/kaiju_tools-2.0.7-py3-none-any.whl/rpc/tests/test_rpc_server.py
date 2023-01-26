import asyncio
from time import time
from uuid import uuid4

import pytest

from ..services import JSONRPCServer
from ..etc import JSONRPCHeaders
from ..jsonrpc import *
from .fixtures import *


@pytest.mark.asyncio
async def test_rpc_server_performance(system_information, rpc_interface, logger):

    counter = 0

    async def _do_call(rpc):
        nonlocal counter
        data = {'method': 'do.sleep', 'params': [1, 2, 3]}
        while 1:
            _id = uuid4()
            data['id'] = _id.int
            await rpc.call(data, {})
            counter += 1

    class _Service(AbstractRPCCompatible):
        @property
        def routes(self) -> dict:
            return {'sleep': self.do_sleep}

        @staticmethod
        def do_sleep(*_, **__):
            return True

    requests, parallel, n = 100000, 32, 5

    print(f'\nJSON RPC Queued Service simple benchmark (best of {n}).')
    print(f'{parallel} connections\n')
    print(system_information)

    async with rpc_interface as rpc:
        rpc.register_service('do', _Service(None))
        tasks = [asyncio.ensure_future(_do_call(rpc)) for _ in range(parallel)]
        t0 = time()
        while counter < requests:
            await asyncio.sleep(0.1)
        t1 = time()
        for task in tasks:
            task.cancel()

    dt = t1 - t0
    rps = round(counter / dt)
    print(f'{dt}')
    print(f'{counter} requests')
    print(f'{rps} req/sec')


@pytest.mark.asyncio
async def test_rpc_server_methods(rpc_interface, rpc_compatible_service, logger):
    logger.info('Testing service context initialization.')

    async with rpc_interface as rpc:

        service = rpc_compatible_service(logger=logger)
        rpc.register_service(service.service_name, service)

        app_id = uuid4()
        correlation_id = uuid4()

        headers = {JSONRPCHeaders.APP_ID_HEADER: app_id, JSONRPCHeaders.CORRELATION_ID_HEADER: correlation_id}

        logger.info('Testing basic requests.')

        data = {'id': uuid4().int, 'method': 'm.echo', 'params': None}
        _headers, response = await rpc.call(data, headers)
        assert response.result == ((), {})

        data = {'id': uuid4().int, 'method': 'm.echo', 'params': {'value': 42}}
        _headers, response = await rpc.call(data, headers)
        assert response.result[1]['value'] == 42

        data = {'id': uuid4().int, 'method': 'm.aecho', 'params': {'a': 1, 'b': 2, 'c': 3}}
        _headers, response = await rpc.call(data, headers)
        assert response.result[1] == {'a': 1, 'b': 2, 'c': 3}

        data = {'id': uuid4().int, 'method': 'm.echo', 'params': {'x': True}}
        _headers, response = await rpc.call(data, headers)
        assert response.result == ((), {'x': True})

        logger.info('Testing data validation.')

        data = {'id': uuid4().int, 'method': 'm.validated', 'params': {'a': 11, 'b': 2}}
        _headers, response = await rpc.call(data, headers)
        assert response.result == 22

        data = {'id': uuid4().int, 'method': 'm.validated', 'params': {'a': 11, 'b': 's'}}
        _headers, response = await rpc.call(data, headers)
        logger.debug(response.repr())
        assert isinstance(response, InvalidParams)

        data = {'id': uuid4().int, 'method': 'm.validated', 'params': {'a': 11}}
        _headers, response = await rpc.call(data, headers)
        logger.debug(response.repr())
        assert isinstance(response, InvalidParams)

        logger.info('Testing multi requests.')

        headers = {}

        data = [
            {'id': uuid4().int, 'method': 'm.echo', 'params': {'x': True}},
            {'id': uuid4().int, 'method': 'm.echo', 'params': {'a': 1, 'b': 2}},
            {'id': uuid4().int, 'method': 'm.aecho', 'params': {'a': 1, 'b': 2}},
        ]
        _headers, response = await rpc.call(data, headers)
        assert [r.result for r in response] == [((), {'x': True}), ((), {'a': 1, 'b': 2}), ((), {'a': 1, 'b': 2})]

        logger.info('Testing request error handling.')

        headers = {}

        data = {'id': uuid4().int, 'method': 'm.unknown', 'params': {'x': True}}
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, MethodNotFound)

        data = {'id': uuid4().int}
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, InvalidRequest)

        data = {'id': uuid4().int, 'method': 'm.unknown', 'params': {'value': True}, 'shit': 1}
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, InvalidRequest)

        data = {'id': uuid4().int, 'method': 'm.sum', 'params': {'x': 1, 'z': '2'}}
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, InvalidParams)

        data = {'id': uuid4().int, 'method': 'm.fail', 'params': None}
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, InternalError)

        logger.info('Testing timeouts.')

        data = {'id': uuid4().int, 'method': 'm.long_echo', 'params': None}
        headers[JSONRPCHeaders.REQUEST_TIMEOUT_HEADER] = 1
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, RequestTimeout)

        data = {'id': uuid4().int, 'method': 'm.long_echo', 'params': None}
        headers[JSONRPCHeaders.REQUEST_TIMEOUT_HEADER] = 10
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response, RPCResponse)

        logger.info('Testing for parallel task execution')

        tasks = []

        for _ in range(4):
            data = {'id': uuid4().int, 'method': 'm.standard_echo', 'params': None}
            headers[JSONRPCHeaders.REQUEST_DEADLINE_HEADER] = int(time() + 1)
            headers[JSONRPCHeaders.CORRELATION_ID_HEADER] = correlation_id
            tasks.append(rpc.call(data, headers))

        t = time()
        await asyncio.gather(*tasks)
        t = time() - t
        assert t <= 1

        logger.info('Testing separate bulk request error handling.')

        data = [
            {'method': 'm.echo', 'params': None},
            {'method': 'm.long_echo', 'params': None},
            {'method': 'm.fail', 'params': None},
            {'method': 'm.sum', 'params': {'x': 1, 'y': 2}},
        ]
        headers[JSONRPCHeaders.REQUEST_DEADLINE_HEADER] = int(time() + 1)
        _headers, response = await rpc.call(data, headers)
        assert isinstance(response[1], RequestTimeout)
        assert isinstance(response[2], RPCError)

        logger.info('All tests finished.')
