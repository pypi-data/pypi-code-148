import pytest
import time
from kortical.api.component_instance import ComponentType
from kortical.app import get_config
from kortical.app import requests
from module_placeholder.api.http_status_codes import HTTP_OKAY


app_config = get_config(format='yaml')
api_key = app_config['api_key']


def with_retries(function, *args, **kwargs):
    retries = 0
    while retries < 600:
        response = function(*args, **kwargs)
        if response.status_code == 200:
            return response
        time.sleep(0.5)
        retries += 1


@pytest.mark.integration
@pytest.mark.smoke
def test_index():
    response = with_retries(requests.get, 'module_placeholder', ComponentType.APP, f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY, response.text
    assert '<body' in response.text


@pytest.mark.integration
@pytest.mark.smoke
def test_predictions():
    test_data = {
        "sport": "Ronaldo scored the goal",
        "tech": "Crypto mining used all the GPUs",
        "politics": "The corrupt rise to leadership positions in all parties",
        "entertainment": "Watching paint dry is an all time classic film",
        "business": "corporate merger, acquisition"
    }

    for category, text in test_data.items():
        request_data = {
            "input_text": text
        }
        response = with_retries(requests.post, 'module_placeholder', ComponentType.APP, f'/predict?api_key={api_key}', json=request_data)
        assert response.status_code == HTTP_OKAY, response.text
        assert response.text == category

