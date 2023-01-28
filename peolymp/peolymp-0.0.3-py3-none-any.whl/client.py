import json

import requests
from eolymp.core.http_client import HttpClient


class HTTPClient(HttpClient):
    def __init__(self, username, password, space):
        resp = requests.post(url='https://api.eolymp.com/oauth/token',
                             data={'username': username, 'password': password,
                                   'grant_type': 'password'})
        token = json.loads(resp.text)['access_token']
        super().__init__(token=token, headers={'Space-ID': space})
