import os
import sys
import pytest

from m360 import constants
from m360.registry import registry_instance
from m360.awareness import instance
from .helper import mock_docker

registry = registry_instance()
awareness = instance()
app_name = "my_app"
ns = "test_ns"
svc = "test_svc"
net = "test_net"
docker_version = "1.24"

constants.MW_TESTING = True

def get_maintenance(config):
    from m360.maintenance import Maintenance
    return Maintenance(config, app_name, registry, "my_service", awareness)

def test_reload_registry_manual(requests_mock):
    # init maintenance library
    maint = get_maintenance({"platform": "manual", "contract": {"ports": {"maintenance": 6000}}})
    reg = {"name": "my_registry", "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    res = maint.reload_registry([])
    assert res
    assert res.get("name") == app_name
    assert res.get("registry") == reg

def test_reload_registry_kubernetes(requests_mock):
    # mock the kube API calls
    constants.SVC_ACCOUNT_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "../assets/kube_token")
    requests_mock.get("https://kubernetes.default.svc/api/v1/namespaces/" + ns + "/endpoints/" + svc,
                      json={"subsets": [{"addresses": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}]},
                                        {"addresses": [{"ip": "10.0.0.3"}]}, {"addresses": [{}]}, {}]})
    # init maintenance library
    maint = get_maintenance({"platform": "kubernetes", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    reg = {"name": "my_registry", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/registry/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/registry/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/registry/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    res = maint.reload_registry([])
    assert res
    assert res.get("name") == app_name
    assert res.get("registry") == reg

def test_reload_registry_docker(requests_mock):
    # mock the docker library's API calls
    cont1 = {"Id": "1234", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.1"}}}}
    cont2 = {"Id": "5678", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.2"}}}}
    cont3 = {"Id": "91011", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.3"}}}}
    containers = [cont1, cont2, cont3]
    mock_docker(containers)
    # init maintenance library
    maint = get_maintenance({"platform": "docker", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    reg = {"name": "my_registry", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/registry/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/registry/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/registry/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    res = maint.reload_registry([])
    assert res
    assert res.get("name") == app_name
    assert res.get("registry") == reg

def test_reload_awareness_1(requests_mock):
    # init maintenance library
    maint = get_maintenance({"platform": "manual", "contract": {"ports": {"maintenance": 6000}}})
    aware = {"name": "complete_awareness", "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": aware})

    res = maint.reload_awareness([])
    assert res
    assert res.get("name") == app_name
    assert res.get("awareness") == aware

def test_reload_awareness_kubernetes(requests_mock):
    # mock the kube API calls
    constants.SVC_ACCOUNT_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "../assets/kube_token")
    requests_mock.get("https://kubernetes.default.svc/api/v1/namespaces/" + ns + "/endpoints/" + svc,
                      json={"subsets": [{"addresses": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}]},
                                        {"addresses": [{"ip": "10.0.0.3"}]}, {"addresses": [{}]}, {}]})
    # init maintenance library
    maint = get_maintenance({"platform": "kubernetes", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    aware = {"name": "complete_awareness", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": aware})

    res = maint.reload_awareness([])
    assert res
    assert res.get("name") == app_name
    assert res.get("awareness") == aware

def test_reload_awareness_docker(requests_mock):
    # mock the docker library's API calls
    cont1 = {"Id": "1234", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.1"}}}}
    cont2 = {"Id": "5678", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.2"}}}}
    cont3 = {"Id": "91011", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.3"}}}}
    containers = [cont1, cont2, cont3]
    requests_mock.get("http+unix:///var/run/docker.sock", json={"result": True})
    requests_mock.get("http+docker://localhost/version", json={"ApiVersion": docker_version})
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/json", json=containers)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont1["Id"] + "/json", json=cont1)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont2["Id"] + "/json", json=cont2)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont3["Id"] + "/json", json=cont3)
    # init maintenance library
    maint = get_maintenance({"platform": "docker", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    aware = {"name": "complete_awareness", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": aware})

    res = maint.reload_awareness([])
    assert res
    assert res.get("name") == app_name
    assert res.get("awareness") == aware

def test_gateway_error(requests_mock):
    # init maintenance library
    maint = get_maintenance({"platform": "manual", "contract": {"ports": {"maintenance": 6000}}})
    # mock the gateway call
    errors = {"520": {"message": "Gateway not available"}}
    requests_mock.get("https://127.0.0.1:5000/registry/", status_code=520, json={"result": False, "errors": errors})

    with pytest.raises(Exception) as e:
        maint.reload_registry([])
    assert "Gateway not available" in str(e)

def test_invalid_kube_token_error(requests_mock):
    # use the wrong path on purpose
    constants.SVC_ACCOUNT_TOKEN_PATH = "/invalid/token"
    # mock the kube API calls
    requests_mock.get("https://kubernetes.default.svc/api/v1/namespaces/" + ns + "/endpoints/" + svc,
                      json={"subsets": [{"addresses": [{"ip": "10.0.0.1"}, {"ip": "10.0.0.2"}]},
                                        {"addresses": [{"ip": "10.0.0.3"}]}, {"addresses": [{}]}, {}]})
    # init maintenance library
    maint = get_maintenance({"platform": "kubernetes", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    reg = {"name": "my_registry", "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    with pytest.raises(Exception) as e:
        maint.reload_registry([])
    assert "No such file or directory" in str(e)

def test_kubernetes_api_error(requests_mock):
    # mock the kube API calls
    constants.SVC_ACCOUNT_TOKEN_PATH = os.path.join(os.path.dirname(__file__), "../assets/kube_token")
    requests_mock.get("https://kubernetes.default.svc/api/v1/namespaces/" + ns + "/endpoints/" + svc,
                      status_code=500, json="")
    # init maintenance library
    maint = get_maintenance({"platform": "kubernetes", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    aware = {"name": "complete_awareness", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": aware})

    with pytest.raises(Exception) as e:
        maint.reload_awareness([])
    assert "Invalid Kubernetes API response" in str(e)

def test_config_error(requests_mock):
    # mock the docker library's API calls
    cont1 = {"Id": "1234", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.1"}}}}
    cont2 = {"Id": "5678", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.2"}}}}
    cont3 = {"Id": "91011", "NetworkSettings": {"Networks": {net: {"IPAddress": "10.0.0.3"}}}}
    containers = [cont1, cont2, cont3]
    requests_mock.get("http+unix:///var/run/docker.sock", json={"result": True})
    requests_mock.get("http+docker://localhost/version", json={"ApiVersion": docker_version})
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/json", json=containers)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont1["Id"] + "/json", json=cont1)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont2["Id"] + "/json", json=cont2)
    requests_mock.get("http+docker://localhost/v" + docker_version + "/containers/" + cont3["Id"] + "/json", json=cont3)
    # init maintenance library
    maint = get_maintenance({"platform": "docker", "contract": {"ports": {"maintenance": 6000}}})
    aware = {"name": "complete_awareness", "_TTL": 5000}
    # mock the brother nodes and gateway calls
    requests_mock.get("https://10.0.0.1:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.2:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://10.0.0.3:6000/awareness/reload", json={"result": True})
    requests_mock.get("https://127.0.0.1:5000/awareness", json={"result": True, "data": aware})

    with pytest.raises(Exception) as e:
        maint.reload_awareness([])
    assert "Configuration must specify 'platformOptions'" in str(e)

def test_docker_env_error(requests_mock):
    try:
        sys.modules.pop("m360")
        sys.modules.pop("m360.maintenance")
        sys.modules.pop("docker")
    except KeyError:
        pass  # ignore errors here
    # init maintenance library
    maint = get_maintenance({"platform": "docker", "contract": {"ports": {"maintenance": 6000}},
                             "platformOptions": {"namespace": ns, "service": svc, "network": net}})
    reg = {"name": "my_registry", "_TTL": 5000}
    # mock the gateway call
    requests_mock.get("https://127.0.0.1:5000/registry/", json={"result": True, "data": {"registry": reg}})

    with pytest.raises(Exception) as e:
        maint.reload_registry([])
    assert "Error while fetching server API version" in str(e)
