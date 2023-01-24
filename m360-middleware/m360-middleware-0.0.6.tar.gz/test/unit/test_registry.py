import pytest

from m360.registry import registry_instance, resource_instance, database_instance, custom_registry_instance

registry = registry_instance()
resource = resource_instance()
database = database_instance()
customreg = custom_registry_instance()

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    registry.clear()  # clear cache so that individual tests don't overlap
    # A test function will be run at this point
    yield
    # Code that will run after each test

def test_get_registry(requests_mock):
    reg = {"name": "my_registry", "config": {"a": 1, "b": "2", "c": True}, "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    res = registry.get()
    assert res == reg
    res = registry.get("config")
    assert res == reg.get("config")
    res = registry.get("_TTL")
    assert res == reg.get("_TTL")
    res = registry.get("invalid")  # should return the whole registry
    assert res == reg

def test_reload_registry(requests_mock):
    reg1 = {"name": "my_registry", "config": {"a": 1, "b": "2", "c": True}, "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg1}})

    res = registry.get()
    assert res == reg1

    reg2 = {"name": "my_new_registry", "config": {"updated": True}, "_TTL": 6000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg2}})

    res = registry.reload()
    assert res == reg2

def test_clear_registry(requests_mock):
    reg1 = {"name": "my_registry", "config": {"a": 1, "b": "2", "c": True}, "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg1}})

    res = registry.reload()
    assert res == reg1

    # mock the gateway call
    reg2 = {"name": "my_new_registry", "config": {"updated": True}, "_TTL": 6000}
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg2}})

    res = registry.get()
    assert res == reg1

    registry.clear()
    res = registry.get()
    assert res == reg2

def test_get_custom_registry(requests_mock):
    reg = {"name": "my_registry", "_TTL": 5000}
    cus = {"cust1": {"a": 1}, "cust2": {"b": "22"}, "cust3": {"c": {"d": "test"}}}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"registry": reg, "custom": cus})
    registry.load()

    res = customreg.get()
    assert res == cus
    res = customreg.get("cust1")
    assert res == cus.get("cust1")
    res = customreg.get("cust2")
    assert res == cus.get("cust2")
    res = customreg.get("cust3")
    assert res == cus.get("cust3")

def test_get_resources(requests_mock):
    reg = {"name": "my_registry", "_TTL": 5000}
    src = {"res1": {"a": 1}, "res2": {"b": "22"}, "res3": {"c": {"d": "test"}}}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"registry": reg, "resources": src})
    registry.load()

    res = resource.get()
    assert res == src
    res = resource.get("res1")
    assert res == src.get("res1")
    res = resource.get("res2")
    assert res == src.get("res2")
    res = resource.get("res3")
    assert res == src.get("res3")

def test_get_databases_single(requests_mock):
    reg = {"name": "my_registry", "_TTL": 5000}
    db = {"single": {"db1": {"name": "db1", "cluster": "cluster_11"}, "db2": {"name": "db2", "cluster": "cluster_22"}}}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"registry": reg, "databases": db})
    registry.load()
    db["single"]["db1"]["cluster"] = {"name": db["single"]["db1"]["cluster"]}
    db["single"]["db2"]["cluster"] = {"name": db["single"]["db2"]["cluster"]}

    res = database.get("single")
    assert res == db.get("single")
    res = database.get("single", "db1")
    assert res == db.get("single").get("db1")
    res = database.get("single", "db2", "tenant1")
    assert res == db.get("single").get("db2")

def test_get_databases_multi(requests_mock):
    db_name = "multi_db"
    reg = {"name": "my_registry", "_TTL": 5000}
    db = {"single": {"db1": {"name": "db1", "cluster": "cluster_11"}},
          "multitenant": {db_name: {"name": db_name, "cluster": "cluster_22"}}}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"registry": reg, "databases": db})
    registry.load()
    db["single"]["db1"]["cluster"] = {"name": db["single"]["db1"]["cluster"]}
    db["multitenant"][db_name]["cluster"] = {"name": db["multitenant"][db_name]["cluster"]}

    res = database.get("single")
    assert res == db.get("single")
    res = database.get("single", "db1", "tenant1")
    assert res == db.get("single").get("db1")
    tenant = "tenant1"
    db["multitenant"][db_name]["name"] = tenant + "_" + db_name
    res = database.get("multitenant", None, tenant)
    assert res == db.get("multitenant")
    res = database.get("multitenant", db_name, "tenant1")
    assert res == db.get("multitenant").get(db_name)
