from typing import Any, Union, Mapping
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from typing import BinaryIO
from tempfile import mkstemp
from pathlib import Path
import zlib
import os
import csv
from io import StringIO
from subprocess import run, DEVNULL

try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files # type: ignore

class ZiptzDialect(csv.Dialect):
    delimiter = '|'
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE
    strict = True


class UnopenedTemporaryFile:
    '''Like NamedTemporaryFile, but not open by default and only with functionality that we need.
    '''
    def __init__(self, *args, **kwargs):
        handle, pathname = mkstemp(*args, **kwargs)
        os.close(handle)
        self.name: Union[str, bytes] = pathname

    def __str__(self) -> str:
        if isinstance(self.name, str):
            return self.name
        else:
            return os.fsdecode(self.name)

    def __bytes__(self) -> bytes:
        if isinstance(self.name, bytes):
            return self.name
        else:
            return os.fsencode(self.name)

    @property
    def path(self) -> Path:
        return Path(str(self.name))

    def __del__(self):
        os.remove(self.name)


class ZiptzBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'ziptz'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__files = []

    def initialize(self, version: str, build_data: Mapping[str, Any]) -> None:
        if self.target_name != 'wheel':
            return

        with StringIO(zlib.decompress((files('hatch_ziptz') / 'tz.data').read_bytes()).decode('utf-8')) as tzio, StringIO() as destination:
            csv.writer(destination).writerows(csv.reader(tzio, dialect=ZiptzDialect))
            tzcsv = destination.getvalue()

        for included in self.build_config.builder.recurse_included_files():
            path = Path(included.path)
            distribution_path = Path(included.distribution_path)
            if distribution_path.name == 'ziptz.csv' and path.stat().st_size == 0:
                output = UnopenedTemporaryFile(suffix='_ziptz.csv')

                with output.path.open('w') as out:
                    out.write(tzcsv)

                self.__files.append(output)
                build_data['force_include'][output.name] = str(distribution_path)
                os.remove(included.path)
