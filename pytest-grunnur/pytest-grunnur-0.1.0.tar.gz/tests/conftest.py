import io

import pytest

from grunnur import API, Context, Device, cuda_api_id, opencl_api_id
from grunnur.api import all_api_ids
from grunnur.adapter_base import APIID
from grunnur.virtual_alloc import TrivialManager, ZeroOffsetManager
from grunnur.testing import (
    MockPyCUDA,
    MockPyOpenCL,
    MockBackendFactory,
)

# Cannot just use the plugin directly since it is loaded before the coverage plugin,
# and all the function definitions in all `grunnur` modules get marked as not covered.
from pytest_grunnur.plugin import (
    context,
    some_context,
    multi_device_context,
    get_devices,
    get_multi_device_sets,
)

from pytest_grunnur.plugin import pytest_addoption as grunnur_pytest_addoption
from pytest_grunnur.plugin import pytest_generate_tests as grunnur_pytest_generate_tests
from pytest_grunnur.plugin import pytest_report_header as grunnur_pytest_report_header


@pytest.fixture
def mock_backend_factory(request, monkeypatch):
    yield MockBackendFactory(monkeypatch)


def pytest_generate_tests(metafunc):
    grunnur_pytest_generate_tests(metafunc)


def pytest_addoption(parser):
    grunnur_pytest_addoption(parser)


def pytest_report_header(config):
    grunnur_pytest_report_header(config)
