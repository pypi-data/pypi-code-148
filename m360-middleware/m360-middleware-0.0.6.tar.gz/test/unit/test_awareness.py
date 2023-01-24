import pytest

from m360.awareness import instance
from m360.utils import from_json
from .helper import Request, random_int, random_string, random_numeric_string

awareness = instance()

def random_user():
    return {
        "id": random_int(1000, 9999),
        "firstname": random_string(15),
        "lastname": random_string(15, uppercase=True),
        "phone": random_numeric_string(8),
        "m360": {
            "m360_prop": "test"
        },
        "tenants": [{
            "id": random_int(1000, 9999),
            "code": "TENANT1"
        }, {
            "id": random_int(1000, 9999),
            "code": "TENANT2"
        }],
        "config": {
            "TENANT1": {"a": 1, "b": 2},
            "TENANT2": {"a": 3, "b": 4}
        }
    }

def random_user_with_config():
    usr = {
        "id": random_int(1000, 9999),
        "email": random_string(15) + "@" + random_string(8) + ".com",
        "firstname": random_string(15),
        "lastname": random_string(15, uppercase=True),
        "status": "active",
        "profile": {"gender": "male", "picture": ""},
        "ts": 1614693465902,
        "account": {
            "_id": "6041ed8e08acbf71381e0789",
            "name": "Corsair M360 - Henotic",
            "ts": 1614613159873,
        },
        "groups": ["admin"],
        "tenants": [{
            "id": "5f2abc6d3b62d4a05c929df9",
            "code": "M360"
        }],
        "config": {
            "common": {"foo": "bar"},
            "specific": {"test": {"foo": "bar"}}
        },
        "auto_registration_flow": "corsair_saas",
        "m360": {}
    }
    usr["m360"]["user"] = {
        "id": usr.get("id"),
        "username": usr.get("username"),
        "firstName": usr.get("firstName"),
        "lastName": usr.get("lastName"),
        "email": usr.get("email"),
        "status": usr.get("status"),
        "profile": usr.get("profile"),
        "ts": usr.get("ts"),
        "account": usr.get("account"),
        "groups": usr.get("groups"),
        "auto_registration_flow": usr.get("auto_registration_flow"),
        "m360": {}
    }
    usr["m360"]["tenants"] = usr.get("tenants"),
    return usr

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    awareness._cache.clear()  # clear cache so that individual tests don't overlap
    # A test function will be run at this point
    yield
    # Code that will run after each test

def test_get_1(requests_mock):
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"success": True})
    res = awareness.get()
    assert res.get("success")

def test_get_2(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/awareness", json={"result": True, "data": {"success": True}})
    res = awareness.get("10.0.0.10", 4000)
    assert res.get("success")

def test_get_3(requests_mock):
    awareness.init(0.00001)  # 1 nanosecond i.e. no cache
    requests_mock.get("https://10.0.0.10:4000/awareness", json={"result": True, "data": {"test": 123}})
    res = awareness.get("10.0.0.10", 4000)
    assert res.get("test") == 123
    requests_mock.get("https://10.0.0.10:4000/awareness", json={"result": True, "data": {"test": 456}})
    res = awareness.get("10.0.0.10", 4000)
    assert res.get("test") == 456
    awareness.init()  # restore to default

def test_reload_1(requests_mock):
    url = "https://127.0.0.1:5000/awareness"
    requests_mock.get(url, json={"test": 123})
    res = awareness.get()
    assert res.get("test") == 123
    requests_mock.get(url, json={"test": 456})
    res = awareness.get()
    assert res.get("test") == 123  # cached value returned
    res = awareness.reload()
    assert res.get("test") == 456  # updated value returned
    res = awareness.get()
    assert res.get("test") == 456  # new cached value returned

def test_reload_2(requests_mock):
    url = "https://10.0.1.10:4000/awareness"
    requests_mock.get(url, json={"test": "ok"})
    res = awareness.get("10.0.1.10", 4000)
    assert res.get("test") == "ok"
    requests_mock.get(url, json={"test": "not ok"})
    res = awareness.get("10.0.1.10", 4000)
    assert res.get("test") == "ok"  # cached value returned
    res = awareness.reload("10.0.1.10", 4000)
    assert res.get("test") == "not ok"  # updated value returned
    res = awareness.get("10.0.1.10", 4000)
    assert res.get("test") == "not ok"  # new cached value returned

def test_get_next_host_1(requests_mock):
    requests_mock.get("https://127.0.0.1:5000/service/nextHost", json={"success": True})
    res = awareness.get_next_host("my_service", 2)
    assert res.get("success")

def test_get_next_host_2(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost", json={"result": True, "data": {"success": True}})
    res = awareness.get_next_host("another_service", 1, "10.0.0.10", 4000)
    assert res.get("success")

def test_proxy_1(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {"ip": "10.11.12.13", "port": 1234}})
    requests_mock.get("https://10.11.12.13:1234/test/route", json={"my_data": {"ok": True}})
    res = awareness.proxy({"service": "another_service", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
                           "route": "/test/route", "qs": {"param1": 123, "param2": "yes"},
                           "headers": {"MY_HEADER": "some-data-goes-here"}})
    assert res.get("my_data").get("ok")

def test_proxy_2(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {"ip": "10.11.12.13", "port": 1234}})
    requests_mock.post("https://10.11.12.13:1234/test/post", json={"my_data": {"ok": True}})
    res = awareness.proxy({"service": "one_service", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
                           "method": "post", "route": "/test/post", "body": {"param1": 123, "param2": "yes"},
                           "headers": {"MY_HEADER": "some-data-goes-here"}})
    assert res.get("my_data").get("ok")

def test_proxy_3(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {}})
    requests_mock.delete("https://127.0.0.1:5000/test/delete", json={"my_data": {"ok": True}})
    res = awareness.proxy({"service": "one_service", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
                           "method": "delete", "route": "/test/delete"})
    assert res.get("my_data").get("ok")

def test_proxy_4(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {"ip": "10.11.12.13", "port": 1234}})
    requests_mock.get("https://10.11.12.13:1234/test/route", json={"my_data": {"ok": True}})
    usr = random_user()
    requests_mock.get("https://127.0.0.1:5000/users/" + str(usr.get("id")), json={"result": True, "data": usr})
    res = awareness.proxy({"service": "another_service", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
                           "route": "/test/route", "qs": {"param1": 123, "param2": "yes"}, "user": usr.get("id"),
                           "headers": {"MY_HEADER": "some-data-goes-here"}})
    assert res.get("my_data").get("ok")

def test_proxy_5(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {"ip": "10.11.12.13", "port": 1234}})
    requests_mock.get("https://10.11.12.13:1234/test/route", json={"my_data": {"ok": True}})
    usr = random_user_with_config()
    requests_mock.get("https://127.0.0.1:5000/users/" + str(usr.get("id")), json={"result": True, "data": usr})
    context = {"service": "test", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
               "route": "/test/route", "qs": {"param1": 123, "param2": "yes"}, "user": usr.get("id"),
               "headers": {"MY_HEADER": "some-data-goes-here"}}
    res = awareness.proxy(context)
    assert res.get("my_data").get("ok")
    assert context.get("headers")
    assert context.get("headers").get("m360")
    m360_headers = from_json(context.get("headers").get("m360"))
    assert m360_headers.get("user")
    assert m360_headers.get("tenants")

def test_proxy_error_1(requests_mock):
    requests_mock.get("https://10.0.0.10:4000/service/nextHost",
                      json={"result": True, "data": {"ip": "10.11.12.13", "port": 1234}})
    requests_mock.get("https://10.11.12.13:1234/test/route", json={"my_data": {"ok": True}})
    requests_mock.get("https://127.0.0.1:5000/users/invalid-id", json={"result": True, "data": None})
    with pytest.raises(Exception) as e:
        awareness.proxy({"service": "another_service", "version": 1, "gatewayIp": "10.0.0.10", "gatewayPort": 4000,
                         "route": "/test/route", "qs": {"param1": 123, "param2": "yes"}, "user": "invalid-id",
                         "headers": {"MY_HEADER": "some-data-goes-here"}})
    assert "User Not Found!" in str(e)
