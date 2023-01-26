from hvclient import Hvclient
import os

def test_token():
    token = os.environ.get('HCV_TOKEN')
    assert isinstance(token, str)

def test_authenticate():
    hvclient = Hvclient()
    assert hvclient.client.is_authenticated()