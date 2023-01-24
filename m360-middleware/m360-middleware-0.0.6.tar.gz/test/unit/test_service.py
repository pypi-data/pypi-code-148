import os
import pytest

from m360 import constants
from m360.service import instance

constants.MW_TESTING = True

service = instance()
DIR_NAME = os.path.dirname(__file__)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before each test
    yield  # A test function will be run at this point
    # Code that will run after each test

def get_config(contract, ip, mwtype, platform, platform_options=None):
    cfg = {
        "ip": ip,
        "type": mwtype,
        "platform": platform
    }
    if contract:
        if type(contract) is str:
            cfg["contract"] = os.path.join(DIR_NAME, "../assets/" + contract)
        else:
            cfg["contract"] = contract
    if platform_options:
        cfg["platformOptions"] = platform_options
    return cfg

def test_register_django_manual(requests_mock):
    config = get_config("contract.json", "localhost", "django", "manual")
    requests_mock.post("https://127.0.0.1:5000/service/register", json={"result": True, "data": config})
    res = service.register(config.get("contract"), config.get("ip"), config)
    assert res == config

def test_register_django_docker(requests_mock):
    config = get_config("contract.json", "localhost", "django", "docker")
    requests_mock.post("https://127.0.0.1:5000/service/register", json={"result": True, "data": config})
    res = service.register(config.get("contract"), config.get("ip"), config)
    assert res == config

def test_register_django_kube(requests_mock):
    config = get_config("contract.json", "localhost", "django", "kubernetes", {"exposedPort": 7000})
    requests_mock.post("https://127.0.0.1:5000/service/register", json={"result": True, "data": config})
    res = service.register(config.get("contract"), config.get("ip"), config)
    assert res == config

def test_register_errors():
    config = get_config(None, "127.0.0.1", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Missing Service Contract!" in str(e)

    config = get_config(" ", "127.0.0.1", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "No such file or directory" in str(e)

    config = get_config("invalid", "127.0.0.1", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "No such file or directory" in str(e)

    contract = {"test": 1, "module": os}
    config = get_config(contract, "127.0.0.1", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Unable to parse the service contract that you provided" in str(e)

    config = get_config("contract.json", None, "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Missing IP Address Value!" in str(e)

    config = get_config("contract.json", "  ", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Missing IP Address Value!" in str(e)

    config = get_config("contract.json", "localhost", "django", "kubernetes")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Missing 'platformOptions' in config" in str(e)

    config = get_config("contract.json", "localhost", "django", "manual")
    with pytest.raises(Exception) as e:
        service.register(config.get("contract"), config.get("ip"), config)
    assert "Connection refused" in str(e)

def test_get_str(requests_mock):
    config = get_config("contract.json", "localhost", "django", "manual")
    requests_mock.get("https://127.0.0.1:5000/service", json={"result": True, "data": config})
    res = service.get(config.get("contract"))
    assert res == config

def test_get_dict(requests_mock):
    config = get_config({"name": "mw-test", "group": "M360GRP"}, "localhost", "django", "manual")
    requests_mock.get("https://127.0.0.1:5000/service", json={"result": True, "data": config})
    res = service.get(config.get("contract"))
    assert res == config

def test_get_errors():
    with pytest.raises(Exception) as e:
        service.get(None)
    assert "Missing Service Contract!" in str(e)

    with pytest.raises(Exception) as e:
        service.get("  ")
    assert "Missing Service Contract!" in str(e)

    with pytest.raises(Exception) as e:
        service.get("/invalid")
    assert "No such file or directory" in str(e)

    contract = {"test": 1, "module": os}
    with pytest.raises(Exception) as e:
        service.get(contract)
    assert "Unable to parse the service contract that you provided" in str(e)

    config = get_config("contract.json", "localhost", "django", "manual")
    with pytest.raises(Exception) as e:
        service.get(config.get("contract"))
    assert "Connection refused" in str(e)

def test_ensure_ip_address():
    res = service.ensure_ip_address({"platform": "manual", "ip": "http://www.google.com"})
    assert res
    res = service.ensure_ip_address({"platform": "kubernetes"})
    assert res

    with pytest.raises(Exception) as e:
        service.ensure_ip_address(None)
    assert "Invalid configuration" in str(e)
    with pytest.raises(Exception) as e:
        service.ensure_ip_address("")
    assert "Invalid configuration" in str(e)
