from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest

from kaiju_tools.tests.fixtures import *
from kaiju_db.tests.fixtures import *


@pytest.fixture()
def files_dir(temp_dir):
    yield temp_dir


@pytest.fixture
def file_service(database_service, application, files_dir, temp_dir, logger):
    from ..files import FileService

    return FileService(application(), database_service=database_service, dir=files_dir, logger=logger)


@pytest.fixture
def sample_file():
    def _file(content: bytes):
        f = NamedTemporaryFile(prefix='pytest', delete=False, mode='wb')
        f.write(content)
        f.close()
        p = Path(f.name)
        return p

    yield _file
