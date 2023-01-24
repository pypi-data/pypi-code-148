import uuid
from pathlib import Path
import os
import shutil
import tempfile
import hashlib
from datetime import datetime, timedelta
from tempfile import TemporaryDirectory
from typing import *

import aiofiles
import sqlalchemy as sa

from kaiju_tools.services import Contextable
from kaiju_tools.rpc.abc import AbstractRPCCompatible
from kaiju_tools.functions import async_run_in_thread
from kaiju_db.services import SQLService, DatabaseService

from .tables import files

__all__ = ['FileService']


class FileService(SQLService, Contextable, AbstractRPCCompatible):
    """File management service which handlers uploads and downloads.

    It's expected to be initialized within a service context manager, but it's possible to do
    initialization manually by directly providing an instance of the database service.

    File service consists of two main parts: file records table and actual files stored in a local
    directory.

    To upload a file first you have to create an empty file record with all metadata about the file
    and then link it to a local file or upload data referencing the record by its id.

    .. code-block:: python

        async with FileService(app, database_service):
            data = await file_service.create({'name': 'test', 'extension': 'txt', 'meta': {'tag': 'file'}})
            data = await file_service.upload_local_file(data['id'], file_path)

    Files are stored locally under their hash UUID and symlinked using their specified names, thus
    same files with different names can coexist in a filesystem and may be served statically via nginx
    or other server.
    """

    service_name = 'files'
    table = files
    URI_PREFIX = '/files/'
    DELETE_UNLINKED_INTERVAL_DAYS = 1

    insert_columns = ('name', 'extension', 'meta')
    update_columns = ('name', 'extension', 'hash', 'meta')

    def __init__(
        self,
        app,
        database_service: DatabaseService,
        dir='.',
        uri_prefix: str = URI_PREFIX,
        permissions=None,
        logger=None,
    ):
        """Initialize.

        :param app:
        :param database_service:
        :param dir: local file storage path
        :param uri_prefix: optional prefix for returned URIs
        :param permissions:
        :param logger:
        """
        super().__init__(app=app, database_service=database_service, logger=logger)
        AbstractRPCCompatible.__init__(self, permissions=permissions)
        self._dir = Path(dir).resolve()
        self._dir.mkdir(exist_ok=True, parents=True)
        self._uri_prefix = Path(uri_prefix)
        self._temp_dir = None
        self.virtual_columns = {'uri': f"'{self._uri_prefix}' || '/' || hash || '/' || name || '.' || extension"}

    @property
    def routes(self) -> dict:
        routes = {**super().routes, 'delete_unlinked': self.delete_unlinked_files}
        return routes

    @property
    def permissions(self) -> dict:
        return {self.DEFAULT_PERMISSION: self.PermissionKeys.GLOBAL_USER_PERMISSION}

    async def init(self):
        self._temp_dir = TemporaryDirectory(prefix='FileService')
        self._temp_dir.__enter__()

    async def close(self):
        if not self.closed:
            self._temp_dir.__exit__(None, None, None)
            self._temp_dir = None

    @property
    def closed(self) -> bool:
        return self._temp_dir is None

    @property
    def temp_dir(self) -> Path:
        return Path(self._temp_dir.name)

    async def upload_local_file(self, id: uuid.UUID, path: Union[str, Path, tempfile.NamedTemporaryFile], move=True):
        """Upload local file.

        Use this method to 'upload' a local file. This operation will move the file into a file service
        directory and link it to a file record.

        :param id: file record id
        :param path: local file path
        :param move: move file instead of copying it
        :return: file and URI
        """
        data = await self.get(id, columns=['name', 'extension', 'meta'])
        _hash = hashlib.md5()
        temp_file = self.get_temp_file_path()
        temp_file.parent.mkdir(exist_ok=True, parents=True)

        if isinstance(path, str):
            pass
        elif isinstance(path, Path):
            path = str(path)
        else:
            path = path.name

        async with aiofiles.open(path, 'rb') as _f:
            size = 1024**2
            chunk = await _f.read(size)
            while chunk:
                _hash.update(chunk)
                chunk = await _f.read(size)

        _hash = uuid.UUID(_hash.hexdigest())
        id, uri = await self._upload(
            file_id=id,
            path=path,
            hash=_hash,
            name=data['name'],
            extension=data['extension'],
            meta=data['meta'],
            _move=move,
        )

        return {'id': id, 'uri': str(uri)}

    async def upload_content(self, id: uuid.UUID, content, _move=True):
        data = await self.get(id, columns=['name', 'extension', 'meta'])
        hash = hashlib.md5()
        temp_file = self.get_temp_file_path()
        temp_file.parent.mkdir(exist_ok=True, parents=True)

        async with aiofiles.open(temp_file, 'wb') as _f:
            async for chunk in content.iter_chunked(1024**2):
                hash.update(chunk)
                await _f.write(chunk)

        hash = uuid.UUID(hash.hexdigest())
        id, uri = await self._upload(
            file_id=id,
            path=temp_file,
            hash=hash,
            name=data['name'],
            extension=data['extension'],
            meta=data['meta'],
            _move=_move,
        )

        return {'id': id, 'uri': str(uri), 'hash': hash, 'tmp_file': temp_file}

    async def delete_unlinked_files(self, days=DELETE_UNLINKED_INTERVAL_DAYS):
        """Remove all old file record which have no hash (i.e. an actual file) linked to them."""
        t = datetime.now() - timedelta(days=days)
        sql = self.table.delete().where(sa.and_(self.table.c.hash == None, self.table.c.timestamp < t))  # noqa alchemy
        await super()._wrap_delete(self._db.execute(sql))

    async def delete_local_file(self, name: Union[Path, str, tempfile.TemporaryFile]):
        if isinstance(name, str):
            pass
        elif isinstance(name, Path):
            name = str(name)
        else:
            name = name.name
        path = Path(name)
        if path.exists():
            await async_run_in_thread(os.unlink, args=(name,))

    async def get_local_file_path(self, id: uuid.UUID):
        file_info = await self.get(id=id, columns=['hash'])
        path = self._get_local_file_path(file_info['hash'])
        return path

    def _get_local_file_path(self, hash: Optional[uuid.UUID]) -> Optional[Path]:
        if hash:
            return self._dir / str(hash) / str(hash)

    def _get_local_file_name(
        self, name: Optional[str], hash: Optional[uuid.UUID], extension: Optional[str]
    ) -> Optional[str]:
        if extension:
            return f'{name}.{extension}'
        elif name:
            return f'{name}'
        elif hash:
            return str(hash)

    def _get_file_uri(self, name: Optional[str], hash: Optional[uuid.UUID], extension: Optional[str]) -> Optional[Path]:
        name = self._get_local_file_name(name=name, hash=hash, extension=extension)
        if name:
            return self._uri_prefix / str(hash) / name

    def _get_local_symlink_path(
        self, name: Optional[str], extension: Optional[str], hash: Optional[uuid.UUID]
    ) -> Optional[Path]:
        name = self._get_local_file_name(name=name, extension=extension, hash=hash)
        if name:
            return self._dir / str(hash) / name

    def get_temp_file_path(self) -> Path:
        temp_file_name = str(uuid.uuid4())
        return self.temp_dir / temp_file_name

    async def get_temp_dir(self, *args, **kws) -> tempfile.TemporaryDirectory:
        kws = {**kws, 'dir': self._temp_dir}
        _dir = await async_run_in_thread(tempfile.TemporaryDirectory, args, kws)
        return _dir

    async def get_temp_file(self, *args, **kws) -> tempfile.NamedTemporaryFile:
        kws = {**kws, 'dir': self._temp_dir}
        temp_file = await async_run_in_thread(tempfile.NamedTemporaryFile, args, kws)
        return temp_file

    def get_temp_file_sync(self, *args, **kws) -> tempfile.NamedTemporaryFile:
        temp_file = tempfile.NamedTemporaryFile(*args, dir=self._temp_dir, **kws)
        return temp_file

    async def _delete_local_files(self, hash: Optional[uuid.UUID]):
        if hash:
            d = self._get_local_file_path(hash).parent
            if d.exists():
                await async_run_in_thread(shutil.rmtree, args=(str(d),))

    async def _upload(
        self,
        file_id: uuid.UUID,
        path: Union[Path, str],
        hash: uuid.UUID,
        name: str,
        extension: str,
        meta: dict,
        _move=True,
    ) -> (uuid.UUID, Path):
        file_path = self._get_local_file_path(hash)
        file_path.parent.mkdir(exist_ok=True, parents=True)
        # uri = self._get_file_uri(name=name, hash=hash, extension=extension)
        if not file_path.exists():
            if _move:
                await async_run_in_thread(shutil.move, args=(str(path), str(file_path)))
            else:
                await async_run_in_thread(shutil.copy, args=(str(path), str(file_path)))
        else:
            await async_run_in_thread(os.unlink, args=(str(path),))
        link = self._get_local_symlink_path(name=name, hash=hash, extension=extension)

        if not link.exists():
            #     sql = self.table.select().with_only_columns([
            #         self.table.c.id
            #     ]).where(
            #         sa.and_(
            #             self.table.c.extension == extension,
            #             self.table.c.name == name,
            #             self.table.c.hash == hash
            #         )
            #     ).limit(1)
            #     data = await super()._wrap_get(self._db.fetchrow(sql))
            #     if data:
            #         await self.delete(file_id, columns=None)
            #         file_id = data['id']
            #         return file_id, uri
            # else:
            await async_run_in_thread(os.symlink, args=(str(file_path), str(link)))

        file_size = file_path.stat().st_size
        meta['file_size'] = file_size
        await self.update(id=file_id, data={'hash': hash, 'meta': meta}, columns=None)
        uri = self._get_file_uri(name=name, hash=hash, extension=extension)
        return file_id, uri

    @staticmethod
    def _create_file(name: str, extension: str = None, meta: dict = None):
        return {'name': name, 'extension': extension, 'meta': {} if meta is None else meta}

    def _insert_uri(self, data):
        data['uri'] = self._get_file_uri(name=data['name'], hash=data['hash'], extension=data['extension'])
