import tempfile
from pathlib import Path

import pytest

from kaiju_tools.tests.fixtures import *
from kaiju_db.tests.fixtures import *
from kaiju_files.tests.fixtures import *
from kaiju_files.converters import FileConverterService


@pytest.fixture
def converter_settings():
    return {
        'ext': ['jpg', 'jpeg'],
        'filename_mask': 'image[0-9]*',
        'directory_mask': None,
        'meta': {
            'some_meta': True,
        },
        'operations': [{'name': 'blur'}],
        'versions': [
            {'version': 'original', 'format': 'png', 'source': 'unprocessed_original'},
            {
                'version': 'resized',
                'format': 'jpeg',
                'source': 'unprocessed_original',
                'operations': [{'name': 'resize', 'params': [200, 200]}],
            },
            {
                'version': 'scaled',
                'format': 'jpeg',
                'source': 'processed_original',
                'operations': [{'name': 'scale', 'params': 0.5}, {'name': 'flip_vertical'}],
                'save_settings': {'quality': 10},
            },
            {
                'version': 'cropped',
                'format': 'png',
                'source': 'previous_version',
                'operations': [{'name': 'aspect_crop', 'params': {'ratio': [1, 1], 'rel_shift': [0.5, 0.5]}}],
                'meta': {'type': 'crop'},
            },
        ],
    }


@pytest.fixture
def image_converter(converter_settings):
    from ..converter import ImageConverter

    with tempfile.TemporaryDirectory() as d:
        converter = ImageConverter(dir=d, settings=converter_settings)
        yield converter


@pytest.fixture
def test_image_file():
    return Path('./kaiju_images/tests/image.jpg')


@pytest.fixture
async def image_service(loop, application, database, database_service, file_service, logger):
    from ..images import ImageService

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
    async with database_service:
        async with file_service:
            yield image_service
