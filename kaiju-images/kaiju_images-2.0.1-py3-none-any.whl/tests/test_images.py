import os
import pathlib

import pytest

from .fixtures import *
from ..images import ImageService


@pytest.mark.asyncio
@pytest.mark.docker
async def test_image_service(
    application, database, database_service, file_service, test_image_file, temp_dir, image_converter, logger
):
    logger.info('Testing image conversion.')
    converter_service = FileConverterService(
        application, database_service=database_service, file_service=file_service, logger=logger
    )
    image_service = ImageService(
        application,
        database_service=database_service,
        file_service=file_service,
        file_converter_service=converter_service,
        logger=logger,
    )
    file_service._temp_dir = temp_dir
    async with database_service:
        async with file_service:
            data = await converter_service.create(
                {'cls': image_converter.__class__.__name__, 'name': 'converter', 'settings': image_converter.settings}
            )
            logger.debug(data)
            converter_id = data['id']
            data = await image_service.file_service.create({'name': 'test', 'extension': 'jpg'})
            file_id = data['id']
            logger.debug(data)
            data = await image_service.file_service.upload_local_file(data['id'], test_image_file, move=False)
            logger.debug(data)
            data = await image_service.convert_from_file(
                file_id=file_id, converter_id=converter_id, metadata={'test': True}
            )
            logger.debug(data)
            assert 'original' in [v['version'] for v in data]

            logger.info('Testing galleries.')
            correlation_id = data[0]['correlation_id']
            data = await image_service.get_gallery(correlation_id)
            logger.debug(data)
            versions = data[0]['versions']
            original_id = versions['original']['id']
            assert versions['original']['original_id'] is None
            versions = tuple(versions.values())
            for version in versions:
                assert version['original_id'] in {None, original_id}
                assert version['correlation_id'] == correlation_id
