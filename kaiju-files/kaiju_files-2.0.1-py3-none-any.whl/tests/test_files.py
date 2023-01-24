from aiohttp.streams import StreamReader

from .fixtures import *


@pytest.mark.asyncio
@pytest.mark.docker
async def test_file_service(database, database_service, file_service, sample_file, logger):
    async with database_service:
        async with file_service:

            logger.info('Testing basic operations.')
            f = await file_service.create({'name': 'test'})
            logger.debug(f)
            meta = await file_service.upload_local_file(f['id'], sample_file(b'test'))
            logger.debug(f)
            assert f['id'] == meta['id']

            # logger.info('Testing deduplication.')
            # f_2 = await file_service.create({'name': 'test'})
            # logger.debug(f_2)
            # meta_2 = await file_service.upload_local_file(f['id'], sample_file(b'test'))
            # logger.debug(meta_2)
            # assert meta_2['id'] != f_2['id'], 'should store file under previous id'
            # assert meta_2['id'] == f['id'], 'should store file under previous id'
