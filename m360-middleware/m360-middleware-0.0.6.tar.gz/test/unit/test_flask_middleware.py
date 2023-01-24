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
from .helper import mock_flask

DIR_NAME = os.path.dirname(__file__)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    yield  # A test function will be run at this point
    # Code that will run after each test
    Helper._instance = None

def test_ssl_cert_error():
    with pytest.raises(SystemExit):
        mock_flask()

def test_validation_errors():
    os.environ["APP_SSL_KEY"] = "true"
    os.environ["APP_SSL_CERT"] = "true"
    with pytest.raises(SystemExit):
        mock_flask()
    with pytest.raises(SystemExit):
        mock_flask({"invalid": "config"})
    with pytest.raises(SystemExit):
        mock_flask({
            "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
            "ip": "localhost",
            "type": "invalid",
            "platform": "manual"
        })
    with pytest.raises(SystemExit):
        mock_flask({
            "contract": "invalid",
            "ip": "localhost",
            "type": "flask",
            "platform": "manual"
        })
    with pytest.raises(SystemExit):
        mock_flask({
            "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
            "type": "flask",
            "platform": "docker"
        })

def test_middleware(requests_mock):
    def special_handler(data):
        data["special"] = True
        return data
    def regular_handler(data):
        data["regular"] = True
        return data
    # setup sdk
    os.environ["APP_SSL_KEY"] = "true"
    os.environ["APP_SSL_CERT"] = "true"
    reg = {"name": "my_registry", "_TTL": 10000}
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})
    requests_mock.post("https://127.0.0.1:5000/service/register", json={"result": True, "data": {}})
    mw = mock_flask(config={
        "contract": os.path.join(DIR_NAME, "../assets/contract.json"),
        "ip": "localhost",
        "type": "flask",
        "platform": "manual"
    }, handler=regular_handler)
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
    req = {"method": "get", "path": "/heartbeat"}
    res = mw(req, special_handler)
    assert res
    assert res.get("heartbeat")
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk

    # test awareness reload
    awareness = {"some-data": "goes here..."}
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": awareness})
    req = {"method": "get", "path": "/awareness/reload"}
    res = mw(req, special_handler)
    assert res
    assert res.get("awareness") == awareness
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk
    assert res.get("special")

    # test registry reload
    req = {"method": "get", "path": "/registry/reload"}
    res = mw(req, special_handler)
    assert res
    assert res.get("registry") == reg
    assert res.get("name") == "mwtest"
    assert instance() is mw.helper.sdk
    assert res.get("special")

    # test regular routes
    req = {"method": "get", "path": "/not/special", "args": {"q1": "string", "q2": 123, "q3": False}}
    res = mw(req, special_handler)
    assert res
    assert res == req
    assert res.get("regular")
    assert instance() is mw.helper.sdk
