import os
import time
import pytest

from m360.sdk import SDK, instance
from m360.awareness import Awareness
from m360.maintenance import Maintenance
from m360.service import Service
from m360.tenant import Tenant
from m360.user import User
from m360.rbac import Rbac
from m360.validator import Validator
from m360.registry import Database, Registry, Resource, CustomRegistry
from m360.frameworks.helper import Helper
from .helper import mock_django, Request

DIR_NAME = os.path.dirname(__file__)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    yield  # A test function will be run at this point
    # Code that will run after each test
    Helper._instance = None

def test_ssl_cert_error():
    with pytest.raises(SystemExit):
        mock_django()

def test_validation_errors():
    os.environ["APP_SSL_KEY"] = "true"
    os.environ["APP_SSL_CERT"] = "true"
    with pytest.raises(SystemExit):
        mock_django()
    with pytest.raises(SystemExit):
        mock_django({"invalid": "config"})
    with pytest.raises(SystemExit):
        mock_django({
            "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
            "ip": "localhost",
            "type": "invalid",
            "platform": "manual"
        })
    with pytest.raises(SystemExit):
        mock_django({
            "contract": "invalid",
            "ip": "localhost",
            "type": "django",
            "platform": "manual"
        })
    with pytest.raises(SystemExit):
        mock_django({
            "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
            "type": "django",
            "platform": "docker"
        })

def test_middleware(requests_mock):
    def handler(request):
        return request.GET
    # setup sdk
    os.environ["APP_SSL_KEY"] = "true"
    os.environ["APP_SSL_CERT"] = "true"
    reg = {"name": "my_registry", "_TTL": 10000}
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})
    requests_mock.post("https://127.0.0.1:5000/service/register", json={"result": True, "data": {}})
    mw = mock_django(config={
        "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
        "ip": "localhost",
        "type": "django",
        "platform": "manual"
    }, handler=handler)
    # wait for lazy init
    time.sleep(0.25)

    # verify SDK
    assert mw
    assert mw.helper
    assert isinstance(mw.helper.sdk, SDK)
    assert isinstance(mw.helper.maintenance, Maintenance)
    assert isinstance(mw.helper.sdk.tenant, Tenant)
    assert isinstance(mw.helper.sdk.user, User)
    assert isinstance(mw.helper.sdk.rbac, Rbac)
    assert isinstance(mw.helper.sdk.awareness, Awareness)
    assert isinstance(mw.helper.sdk.registry, Registry)
    assert isinstance(mw.helper.sdk.custom, CustomRegistry)
    assert isinstance(mw.helper.sdk.database, Database)
    assert isinstance(mw.helper.sdk.resource, Resource)
    assert isinstance(mw.helper.sdk.service, Service)
    assert isinstance(mw.helper.sdk.validator, Validator)
    # stop the timers (not needed for this test)
    mw.helper.sdk.stop_auto_reload()

    # test heartbeat
    req = Request(path="/heartbeat")
    res = mw(req)
    assert res
    assert res.get("heartbeat")
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk

    # test awareness reload
    awareness = {"some-data": "goes here..."}
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": awareness})
    req = Request(path="/awareness/reload")
    res = mw(req)
    assert res
    assert res.get("awareness") == awareness
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk

    # test registry reload
    req = Request(path="/registry/reload")
    res = mw(req)
    assert res
    assert res.get("registry") == reg
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk

    # test regular routes
    req = Request(path="/not/special")
    params = {"q1": "string", "q2": 123, "q3": False}
    req.GET = params
    res = mw(req)
    assert res == params
    assert instance() is mw.helper.sdk
