import pytest
from kortical.app import get_config
from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_config(format='yaml')
api_key = app_config['api_key']


@pytest.mark.unit
def test_index_endpoint(client):
    response = client.get(f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY


@pytest.mark.unit
def test_predict_endpoint(client):
    request_data = {
        "input_text": "Hello this is some input text"
    }
    response = client.post(f'/predict?api_key={api_key}', json=request_data)
    assert response.status_code == HTTP_OKAY


@pytest.mark.unit
def test_predict_endpoint_no_api_key(client):
    response = client.post(f'/predict')
    assert response.status_code == UNAUTHORISED


@pytest.mark.unit
def test_predict_endpoint_wrong_api_key(client):
    response = client.post(f'/predict?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED
