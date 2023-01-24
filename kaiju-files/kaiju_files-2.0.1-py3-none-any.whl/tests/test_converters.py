from aiohttp.streams import StreamReader

from .fixtures import *
from ..abc import AbstractFileConverter
from ..converters import converters, FileConverterService


@pytest.mark.asyncio
@pytest.mark.docker
async def test_file_converter_service(application, database, database_service, file_service, sample_file, logger):
    class ToUpperTextConverter(AbstractFileConverter):

        source = None

        def _convert(self, input_buffer, **metadata):
            output_file = self._create_file()
            f = input_buffer.read()
            with output_file:
                output_file.write(f.upper())
                """Do here what you need and return your
                 output file path and additional data."""
            self.__class__.source = f
            yield output_file, metadata

    converters.register_class(ToUpperTextConverter)
    s = 'test'

    converter_service = FileConverterService(
        application(), database_service=database_service, file_service=file_service, logger=logger
    )

    async with database_service:
        async with file_service:

            logger.info('Testing converter construction.')
            data = {
                'cls': 'ToUpperTextConverter',
                'name': 'converter',
                'settings': {'ext': ['test'], 'meta': {'test': True}},
            }
            result = await converter_service.create(data)
            logger.debug(result)

            logger.info('Testing file conversion using a converter.')
            f = await converter_service.file_service.create({'name': 'test'})
            logger.debug(f)
            f = await converter_service.file_service.upload_local_file(f['id'], sample_file(s.encode()))
            logger.debug(f)
            result = await converter_service.convert(result['id'], f['id'], metadata={'test2': True})
            logger.debug(result)
            version = result['versions'][0]
            assert version['meta']['test'] is True and version['meta']['test2'] is True
            assert ToUpperTextConverter.source == s.encode()
            version_file_id = version['file']['id']
            f = await converter_service.file_service.get_local_file_path(version_file_id)
            with open(f, 'r') as f:
                result = f.read()
            assert result == s.upper(), 'version file should have a processed string inside'
