import pytest

from m360.utils import to_json
from m360.tenant import instance
from .helper import Request, random_int, random_string, random_numeric_string

tenant = instance()

def random_tenant():
    return {
        "id": random_int(1000, 9999),
        "code": random_string(8, uppercase=True),
        "name": random_string(15),
        "description": random_string(50),
        "phone": random_numeric_string(8)
    }

def random_tenants(count=random_int(3, 6)):
    arr = []
    for i in range(count):
        arr.append(random_tenant())
    return arr

def test_get():
    count = random_int(4, 7)
    ten = random_tenants(count)
    req = Request(headers={"m360": to_json({"tenants": ten}), "another-header": "--Some Value--"})

    for i in range(count):
        res = tenant.get(req, ten[i].get("code"))
        assert res == ten[i]

def test_list():
    ten = random_tenants()
    req = Request(headers={"m360": to_json({"tenants": ten}), "another-header": "--Some Value--"})

    res = tenant.list(req)
    assert res == ten

def test_find_one(requests_mock):
    ten = random_tenant()
    requests_mock.post("https://127.0.0.1:5000/tenants", json={"result": True, "data": ten})

    res = tenant.find([ten.get("code")])
    assert res == ten

def test_find_many(requests_mock):
    count = random_int(4, 7)
    ten = random_tenants(count)
    requests_mock.post("https://127.0.0.1:5000/tenants", json={"result": True, "data": ten})

    res = tenant.find()
    assert res == ten

def test_get_errors():
    count = random_int(4, 7)
    ten = random_tenants(count)
    req1 = Request(headers={"another-header": "--Some Value--"})
    req2 = Request(headers={"m360": '[]-{"invalid-json"}', "another-header": "--Some Value--"})
    req3 = Request(headers={"m360": to_json({"missing-tenants": ten}), "another-header": "--Some Value--"})
    req4 = Request(headers={"m360": to_json({"tenants": ten}), "another-header": "--Some Value--"})

    assert not tenant.get(req1, ten[0].get("code"))
    assert not tenant.get(req2, ten[0].get("code"))
    assert not tenant.get(req3, ten[0].get("code"))
    assert not tenant.get(req4, "inv-code")

def test_list_errors():
    req1 = Request(headers={"another-header": "--Some Value--"})
    req2 = Request(headers={"m360": '[]-{"invalid-json"}', "another-header": "--Some Value--"})
    req3 = Request(headers={"m360": to_json({"missing-tenants": random_tenants()}), "another-header": "--Some Value--"})
    req4 = Request(headers={"m360": to_json({"tenants": random_tenant()}), "another-header": "--Some Value--"})

    assert not tenant.list(req1)
    assert not tenant.list(req2)
    assert not tenant.list(req3)
    assert not tenant.list(req4)

def test_find_errors():
    with pytest.raises(Exception) as e:
        tenant.find()
    assert "Connection refused" in str(e)
