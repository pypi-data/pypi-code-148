# SPDX-License-Identifier: MIT

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

import pytest


@pytest.fixture
def tmpdir() -> Iterator[Path]:
    with TemporaryDirectory() as directory:
        yield Path(directory)
