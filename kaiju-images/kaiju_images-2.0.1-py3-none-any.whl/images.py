import asyncio
import uuid
from enum import Enum
from typing import List, Optional, Union

import sqlalchemy as sa

from kaiju_tools.rpc import AbstractRPCCompatible
from kaiju_db.services import DatabaseService, SQLService
from kaiju_files.services import FileService, FileConverterService
from kaiju_tools.exceptions import ValidationError

from kaiju_images.tables import images

__all__ = ['ImageService']


class ImageService(SQLService, AbstractRPCCompatible):
    """
    This service manages images including storage / conversion and galleries.

    The concept is that you have an image file linked both to a file service and to an image service.
    Each image file may have different versions (sizes, colors etc.) derived from image converters.
    Such versions are interlinked using the `original_id` attribute present in each row
    (except original itself).
    Also there's an option to create a "gallery" - an arbitrary user collection of images.
    It is managed by the `correlation_id` attribute.

    .. code-block:: python

        {
          "id": "",             # image unique id
          "version",            # version string (as in converters, for the original it's `None`)
          "correlation_id": "", # arbitrary correlation id to link different images in a gallery
          "original_id": "",    # link to an original image id (for the original it's always `None`)
          "file_id": "",        # link to a file object id in file service table
          "metadata": {}        # additional metadata from converters / user / image service
        }

    To create an image use a default `SQLService.create` method.

    If you want to use a converter instead to create multiple version, you can use a provided method.

    .. code-block:: python

            images = await image_service.convert_from_file(
            file_id=file_id, converter_id=converter_id, metadata={'test': True})

    You can access galleries by correlation id using such method:

    .. code-block:: python

        gallery = await image_service.get_gallery(correlation_id)

    """

    class Versions(Enum):
        original = None

    service_name = 'images'
    table = images
    file_service = FileService
    converter_classes = ['ImageConverter']

    def __init__(
            self, app,
            database_service: DatabaseService,
            file_service: FileService = None,
            file_converter_service: FileConverterService = None,
            permissions=None, logger=None
    ):
        """
        :param app:
        :param database_service:
        :param file_service:
        :param file_converter_service:
        :param logger:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)
        self.file_service = self.discover_service(file_service)
        self.converters_service = self.discover_service(file_converter_service, required=False)

    @property
    def routes(self) -> dict:
        return {
            **super().routes,
            'convert': self.convert_image,
            'convert_from_file': self.convert_from_file,
            'gallery': self.get_gallery,
            'versions.delete': self.delete_versions,
            'converters.list': self.list_converters
        }

    async def list_converters(self, *args, conditions=None, **kws):
        cond = {
            'cls': self.converter_classes
        }
        if not conditions:
            conditions = cond
        else:
            conditions.update(cond)

        return await self.converters_service.list_converters(conditions=conditions, *args, **kws)

    async def _convert_file(
            self, original_id, converter_id, file_id, converter_settings,
            metadata, correlation_id, columns: Optional[Union[str, List[str]]] = '*', file_path=None):

        if self.converters_service is None:
            raise RuntimeError('Converter service is not available.')

        original, converter_data = await asyncio.gather(
            self.get(id=original_id, columns=columns),
            self.converters_service.convert(
                id=converter_id, file_id=file_id, file_path=file_path, settings=converter_settings,
                metadata=metadata)
        )
        versions = converter_data['versions']
        data = [
            {
                'file_id': version['file']['id'],
                'original_id': original_id,
                'version': version['meta']['version'],
                'meta': version['meta'],
                'correlation_id': correlation_id
            }
            for version in versions
        ]
        data = await self.m_create(data, columns=columns)
        return [original, *data]

    async def convert_image(
            self, id: uuid.UUID, converter_id: uuid.UUID,
            converter_settings: dict = None, metadata: dict = None,
            columns: Optional[Union[str, List[str]]] = '*'):
        """Converts an image with a converter and saves all its versions.
        The image must be of original version.
        """

        original = await self.get(id=id, columns=['file_id', 'version', 'correlation_id'])
        if original['version'] != self.Versions.original.value:
            raise ValidationError('Image version must be "%s".' % self.Versions.original.value)
        file_id = original['file_id']
        correlation_id = original['correlation_id']
        return await self._convert_file(
            original_id=id, file_id=file_id, converter_id=converter_id,
            converter_settings=converter_settings, metadata=metadata,
            correlation_id=correlation_id, columns=columns)

    async def convert_from_file(
            self, file_id: uuid.UUID, converter_id: uuid.UUID,
            converter_settings: dict = None, metadata: dict = None,
            correlation_id: uuid.UUID = None,
            columns: Optional[Union[str, List[str]]] = '*'):
        """Converts file with a converter. This function will create an original
        version record as well.
        """

        original = await self.create({
            'file_id': file_id,
            'original_id': None,
            'version': None,
            'meta': metadata,
            'correlation_id': correlation_id
        })
        original_id = original['id']
        if correlation_id is None:
            correlation_id = original_id
            sql = self.table.update().where(
                self.table.c.id == original_id
            ).values(
                correlation_id=correlation_id
            )
            await self._wrap_update(self._db.execute(sql))
        return await self._convert_file(
            original_id=original_id, file_id=file_id, converter_id=converter_id,
            converter_settings=converter_settings, metadata=metadata,
            correlation_id=correlation_id, columns=columns)

    async def get_gallery(self, id: Union[uuid.UUID, List[uuid.UUID]]):
        """Returns a gallery with all available most recent versions of images.

        :param id: list of correlation id
        """

        if isinstance(id, uuid.UUID):
            id = [id]

        sql = self.table.select().distinct(
            self.table.c.correlation_id,
            self.table.c.version
        ).where(
            self.table.c.correlation_id.in_(id)
        ).order_by(
            self.table.c.correlation_id,
            self.table.c.version,
            self.table.c.timestamp.desc()
        )
        data = await self._wrap_get(self._db.fetch(sql))

        files = [row['file_id'] for row in data]
        files = await self.file_service.m_get(id=files)
        files = {row['id']: row for row in files}

        result = {}
        order = {_id: n for n, _id in enumerate(id)}

        for row in data:
            row = dict(row)
            file_id = row['file_id']
            image_id = row['correlation_id']
            if not image_id:
                image_id = row['id']
            file_info = files[file_id]
            row['file'] = file_info
            version = row['version']
            if version is None:
                version = 'original'

            if image_id in result:
                result[image_id]['versions'][version] = row
            else:
                result[image_id] = {'id': image_id, 'versions': {version: row}}

        result = list(result.values())
        result.sort(key=lambda x: order.get(x['id'], 0))
        return result

    async def delete_versions(
            self, id: Union[uuid.UUID, List[uuid.UUID]], versions: Union[str, List[str]],
            columns: Optional[Union[str, List[str]]] = '*'):
        """Remove particular versions of images.

        :param id: list of original image ids
        :param versions: list of image versions (excl. "original")
        :param columns: columns to return
        """

        if isinstance(id, uuid.UUID):
            ids = [id]
        else:
            ids = id
        if isinstance(versions, str):
            versions = [versions]
        if self.Versions.original.value in versions:
            raise ValidationError(
                'Deleting image originals is prohibited.'
                ' Use "delete" method instead to remove the whole version tree.')
        sql = self.table.delete().where(
            sa.and_(
                self.table.c.original_id.in_(ids),
                self.table.c.version.in_(versions)
            )
        )
        if columns:
            columns = self._sql_get_columns(columns)
            sql = sql.returning(*columns)
            if isinstance(id, uuid.UUID):
                data = await self._wrap_delete(self._db.fetchrow(sql))
            else:
                data = await self._wrap_delete(self._db.fetch(sql))
            return data
        else:
            await self._wrap_delete(self._db.execute(sql))

    @staticmethod
    def _get_correlation_id():
        return uuid.uuid4()

    def prepare_insert_data(self, session, data: dict):
        file_id = data['file_id']
        original_id = data.get('original_id', None)
        correlation_id = data.get('correlation_id', None)
        version = data.get('version', None)
        meta = data.get('meta', None)
        data = self._create_image(
            file_id=file_id, original_id=original_id, version=version,
            correlation_id=correlation_id, meta=meta)
        return data

    def _create_image(
            self, file_id: uuid.UUID, original_id: uuid.UUID = None, version: str = None,
            correlation_id: uuid.UUID = None, meta: dict = None, **_):
        if version is None:
            version = self.Versions.original.value
        if version != self.Versions.original.value:
            if not original_id:
                raise ValueError('Image of version "%s" must have "original_id".' % version)
        if correlation_id is None:
            correlation_id = self._get_correlation_id()
        data = {
            'version': version,
            'file_id': file_id,
            'original_id': original_id,
            'correlation_id': correlation_id,
            'meta': meta if meta else {}
        }
        return data
