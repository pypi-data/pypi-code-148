from m360.gateway.connector import instance

connector = instance()

def test_invoke_1(requests_mock):
    requests_mock.get("https://127.0.0.1:5000", json={"success": True})
    res = connector.invoke()
    assert res.get("success")

def test_invoke_2(requests_mock):
    requests_mock.get("https://10.0.0.1:4000", json={"result": True, "data": {"success": True}})
    res = connector.invoke({"ip": "10.0.0.1", "port": 4000})
    assert res.get("success")

def test_invoke_3(requests_mock):
    connector.init("my_service", "1.2.3")
    requests_mock.post("https://10.0.0.1:5000/test/route", json={"result": True, "data": {"test": {"success": True}}})
    res = connector.invoke({"ip": "http://10.0.0.1//", "route": "/test/route", "method": "post",
                            "headers": {"XXX": "123"}, "qs": {"q1": "val1", "q2": 2},
                            "body": {"obj": {"name": "hg", "active": True, "details": {"address": "BEY"}}}})
    assert res.get("test").get("success")
