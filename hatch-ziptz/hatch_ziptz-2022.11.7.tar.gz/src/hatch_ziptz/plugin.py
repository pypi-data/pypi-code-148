from typing import Any, Optional, Union, Mapping, MutableMapping, NamedTuple, List, MutableSequence, Sequence
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from typing import BinaryIO
from tempfile import mkstemp
from pathlib import Path
import zlib
from contextlib import ExitStack
import os
import csv
from io import StringIO
from subprocess import run, DEVNULL
try:
    import ujson as json # type: ignore
except ImportError:
    import json

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

class TzEntry(NamedTuple):
    name: str
    dst: bool
    offset: Optional[int] = None

    def dict(self) -> Mapping[str, Any]:
        output = {
            'name': self.name,
            'dst': self.dst,
        }
        if self.offset is not None:
            output['offset'] = self.offset

        return output


class ZiptzBuildHook(BuildHookInterface):
    PLUGIN_NAME = 'ziptz'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__files = []

    def initialize(self, version: str, build_data: MutableMapping[str, Any]) -> None:
        if self.target_name != 'wheel':
            return

        dest = self.config['destination']

        offsets = {}

        with StringIO(zlib.decompress((files('hatch_ziptz') / 'tzm.data').read_bytes()).decode('utf-8')) as tzmio:
            for row in csv.DictReader(tzmio, fieldnames=('tz', 'offset'), dialect=ZiptzDialect):
                offsets[row['tz']] = int(row['offset'])

        timezones: MutableSequence[TzEntry] = []
        timezones_map: MutableMapping[TzEntry, int] = {}

        zipcodes: MutableMapping[str, int] = {}

        with StringIO(zlib.decompress((files('hatch_ziptz') / 'tz.data').read_bytes()).decode('utf-8')) as tzio:
            for row in csv.DictReader(tzio, fieldnames=('zip', 'tz', 'dst'), dialect=ZiptzDialect):
                entry = TzEntry(
                    name=row['tz'],
                    dst=bool(int(row['dst'])),
                    offset=offsets.get(row['tz']),
                )

                if entry in timezones_map:
                    index = timezones_map[entry]
                else:
                    index = len(timezones)
                    timezones.append(entry)
                    timezones_map[entry] = index

                zipcodes[row['zip']] = index

        output = UnopenedTemporaryFile(suffix='_ziptz.json')

        payload = {
            'timezones': [entry.dict() for entry in timezones],
            'zipcodes': zipcodes,
        }

        with output.path.open('w') as out:
            json.dump(payload, out)

        self.__files.append(output)
        build_data['force_include'][output.name] = dest
