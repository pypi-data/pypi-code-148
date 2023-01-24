from typing import Type, List
from uuid import UUID

try:
    from typing import TypedDict
except ImportError:
    # python 3.6 compatibility
    from typing_extensions import TypedDict

from kaiju_db import SQLService, DatabaseService
from kaiju_tools.class_registry import AbstractClassRegistry
from kaiju_tools.exceptions import NotFound, ValidationError
from kaiju_tools.mapping import recursive_update
from kaiju_tools.services import Service, Contextable
from kaiju_tools.functions import async_run_in_thread
from kaiju_files.abc import AbstractFileConverter
from kaiju_files.etc import ErrorCodes
from kaiju_files.tables import converters as converters_table
from kaiju_files.files import FileService

__all__ = ['ErrorCodes', 'FileConverterService', 'converters', 'FileConvertersRegistry']


class FileConvertersRegistry(AbstractClassRegistry):
    """Registry of all file converters."""

    base_classes = (AbstractFileConverter,)


converters = FileConvertersRegistry()


class FileConverterService(SQLService):
    """File converters storage and execution.

    You can use it for image and other data types conversion.

    First if you need a specific converter class you should inherit it from `AbstractFileConverter`
    interface and register it in `converters` class registry.

    .. code-block:: python

        from kaiju_files.abc import AbstractFileConverter
        from kaiju_files.converters import converters

        class MyConverterClass(AbstractFileConverter):
            ...

        converters.register_class(MyConverterClass)


    From now you can use it in you converter service. It's best to init this service within a
    service context manager but you can init it directly by providing instances of a database
    service and a file service. Then you can save your converter settings and convert files
    using your converter.

    .. code-block:: python

        my_converter_settings = {...}

        async with FileConverterService(...) as fcs:
            row = {'cls': 'MyConverterClass', 'name': 'my converter', 'settings': my_converter_settings}
            row = await fcs.create(row)
            versions_info = await fsc.convert(row['id'], my_file_id)

    """

    service_name = 'FileConverter'
    MAX_PROCESSING_TIME = 300
    table = converters_table
    update_columns = {'system', 'settings'}

    class _ConvertedFileInfo(TypedDict):
        class _ConvertedVersionInfo(TypedDict):
            name: str
            extension: str
            meta: dict

        file_id: UUID
        converter_id: UUID
        versions: List[_ConvertedVersionInfo]

    def __init__(
        self,
        app,
        database_service: DatabaseService,
        file_service: FileService = False,
        converters=converters,
        max_processing_time=MAX_PROCESSING_TIME,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param database_service:
        :param file_service:
        :param converters: converters registry (uses default registry)
        :param max_processing_time: conversion time limit (sec)
        :param logger:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        self.file_service = self.discover_service(file_service)
        self.converters = converters
        self.max_processing_time = max(1, int(max_processing_time))

    @property
    def routes(self) -> dict:
        return {**super().routes, 'classes': self.get_converter_class_specs, 'call': self.convert}

    async def get_converter_class_specs(self, cls: str = None):
        """Return a list of registered converter classes specification."""
        if cls:
            _cls = self._get_converter_class(cls)
            return {'cls': cls, 'spec': _cls.spec()}
        else:
            return [{'cls': cls, 'spec': _cls.spec()} for cls, _cls in self.converters.items()]

    async def convert(self, id, file_id, settings: dict = None, metadata: dict = None, **__) -> _ConvertedFileInfo:
        """Convert a file.

        :param id: converter ID
        :param file_id: file to convert
        :param settings: additional converter settings
        :param metadata: additional metadata
        :return:
        """
        base_file_info = await self.file_service.get(file_id, columns=['name', 'extension', 'meta', 'hash'])
        base_meta = base_file_info['meta']

        if metadata is None:
            metadata = base_meta
        else:
            base_meta.update(metadata)
            metadata = base_meta

        file_path = self.file_service._get_local_file_path(base_file_info['hash'])
        if not file_path.exists():
            raise RuntimeError('Local file referenced by this id (%s) doesn\'t exist.' % file_id)
        converter = await self.init_converter(id, settings)
        kws = {**metadata, 'return_exceptions': True, 'max_exec_time': converter.max_processing_time}
        result = await async_run_in_thread(converter.convert, (file_path,), kws)
        data = []

        if isinstance(result, Exception):
            raise result

        for f, meta in result:
            version_name = meta.get('version')
            if not version_name:
                version_name = self.converters.class_key(converter)
            output_ext = meta.get('output_extension')
            if not output_ext:
                output_ext = base_file_info['extension']
            name = meta.get('name')
            if not name:
                name = base_file_info['name']
            name = f'{name}__{version_name}'
            version = {'name': name, 'extension': output_ext, 'meta': meta}
            file_info = await self.file_service.create(version)
            try:
                file_info = await self.file_service.upload_local_file(file_info['id'], f.name)
            except Exception:
                await self.file_service.delete_local_file(f.name)
                raise
            else:
                version['file'] = file_info
                data.append(version)

        return {'file_id': file_id, 'converter_id': id, 'versions': data}

    def prepare_insert_data(self, session, data: dict) -> dict:
        cls, settings = data['cls'], data['settings']
        converter = self._create_converter(cls, settings)
        return {
            'cls': self.converters.class_key(converter),
            'name': data['name'],
            'system': data.get('system', False),
            'settings': converter.settings.repr(),
        }

    def _get_converter_class(self, cls: str) -> Type[AbstractFileConverter]:
        if cls not in self.converters:
            keys = self.converters.keys()
            raise NotFound(
                'Converter class doesn\'t exist.',
                key=cls,
                available_classes=list(keys),
                code=ErrorCodes.NO_CONVERTER_CLASS_FOUND,
            )
        return self.converters[cls]

    async def init_converter(self, id, settings=None) -> AbstractFileConverter:
        """Return a converter instance ready to use.

        :param id: converter ID
        :param settings: additional settings to update default settings
        """
        converter = await self.get(id, columns='*')
        if settings:
            settings = recursive_update(converter['settings'], settings)
        else:
            settings = converter['settings']
        converter = self._create_converter(converter['cls'], settings)
        if isinstance(converter, Contextable):
            await converter.init()
        return converter

    def _create_converter(self, cls: str, settings: dict) -> AbstractFileConverter:
        """Create a new converter object from a class name and settings dict.

        :param cls: class name as in converters registry (uses `class.__name__` by default)
        """
        cls = self._get_converter_class(cls)
        try:
            if issubclass(cls, Service):
                converter = cls(
                    app=self.app,
                    logger=self.logger,
                    dir=self.file_service.temp_dir,
                    settings=settings,
                    max_processing_time=self.max_processing_time,
                )
            else:
                converter = cls(
                    dir=self.file_service.temp_dir, settings=settings, max_processing_time=self.max_processing_time
                )
        except (ValueError, AttributeError, TypeError) as e:
            raise ValidationError(
                'Invalid converter settings.', base_exc=e, converter_cls=cls, code=ErrorCodes.INVALID_CONVERTER_SETTINGS
            )
        else:
            return converter
