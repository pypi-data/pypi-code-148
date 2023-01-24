import pytest

from m360.utils import to_json
from m360.user import instance
from .helper import Request, random_int, random_string, random_numeric_string

user = instance()

def random_user():
    return {
        "id": random_int(1000, 9999),
        "firstname": random_string(15),
        "lastname": random_string(15, uppercase=True),
        "phone": random_numeric_string(8)
    }

def random_users(count=random_int(3, 6)):
    arr = []
    for i in range(count):
        arr.append(random_user())
    return arr

def test_get():
    usr = random_user()
    req = Request(headers={"m360": to_json({"user": usr}), "another-header": "--Some Value--"})

    res = user.get(req)
    assert res == usr

def test_find_one(requests_mock):
    usr = random_user()
    requests_mock.get("https://127.0.0.1:5000/users/" + str(usr.get("id")), json={"result": True, "data": usr})

    res = user.find({"id": usr.get("id"), "tenant": "XYZ", "group": "GRP1", "service": "aaa", "version": 1})
    assert res == usr

def test_find_many(requests_mock):
    count = random_int(4, 7)
    usr = random_users(count)
    requests_mock.get("https://127.0.0.1:5000/users?start=2&limit=5", json={"result": True, "data": usr})

    res = user.find({"start": 2, "limit": 5})
    assert res == usr

def test_get_errors():
    count = random_int(4, 7)
    usr = random_users(count)
    req1 = Request(headers={"another-header": "--Some Value--"})
    req2 = Request(headers={"m360": '[]-{"invalid-json"}', "another-header": "--Some Value--"})
    req3 = Request(headers={"m360": to_json({"missing-users": usr}), "another-header": "--Some Value--"})
    req4 = Request(headers={"m360": to_json({"user": None}), "another-header": "--Some Value--"})

    assert not user.get(req1)
    assert not user.get(req2)
    assert not user.get(req3)
    assert not user.get(req4)

def test_find_errors():
    with pytest.raises(Exception) as e:
        user.find({})
    assert "Connection refused" in str(e)

