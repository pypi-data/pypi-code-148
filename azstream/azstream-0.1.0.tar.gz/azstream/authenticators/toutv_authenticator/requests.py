from typing import Dict
from base64 import b64encode
from urllib.parse import urlencode
from .consts import PROFILE_URL, PROFILE_HEADERS
from copy import deepcopy


def get_login_request_data(
    username: str, 
    password: str,
    scopes: str,
    app_user_agent: str,
    client_id: str,
    client_secret: str,
    device_type: str
) -> tuple[str, Dict[str, str]]:
    body_dict = None
    headers = None
    if device_type == 'phone':
        body_dict = {
            'grant_type': 'password',
            'client_id': client_id,
            'client_secret': client_secret,
            'username': username,
            'password': password,
            'scope': scopes,
            'response_type': 'id_token'
        }
        headers = {
            'accept-encoding': 'gzip',
            'connection': 'Keep-Alive',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': app_user_agent
        }
    elif device_type == 'tv':
        body_dict = {
            'grant_type': 'password',
            'client_id': client_id,
            'username': username,
            'password': password,
            'scope': scopes,
            'response_type': 'token'
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'identity',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': app_user_agent
        }
    body = urlencode(body_dict)
    return body, headers

def get_refresh_request_data(
    refresh_token: str,
    app_user_agent: str,
    device_type: str,

) -> tuple[str, Dict[str, str]]:
    body_dict = None
    headers = None
    if device_type == 'phone':
        body_dict = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = {
            'accept-encoding': 'gzip',
            'connection': 'Keep-Alive',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': app_user_agent
        }
    elif device_type == 'tv':
        body_dict = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'identity',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': app_user_agent
        }
    body = urlencode(body_dict)
    return body, headers

def get_profile_request_data(
    access_token: str,
    device_id: str
) -> tuple[str, Dict[str, str]]:
    url = PROFILE_URL
    headers = deepcopy(PROFILE_HEADERS)
    headers['authorization']    = headers['authorization'].format(access_token=access_token)
    headers['x-rc-device-id']   = headers['x-rc-device-id'].format(device_id=device_id)
    headers['x-requested-with'] = headers['x-requested-with'].format(device_id=device_id)
    return url, headers

def generate_basic_token(credentials: tuple[str, str]) -> str:
    return b64encode(f'{credentials[0]}:{credentials[1]}'.encode()).decode()