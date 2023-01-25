from typing import Tuple, Dict
from urllib.parse import urlencode
from copy import deepcopy
from .consts import *


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# SETTINGS                                                                    #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def get_settings_request_data(
    device_type: str, 
    client_id: str,
    app_user_agent: str
) -> tuple[str, Dict[str, str]]:
    headers = None
    url = None
    if device_type == 'phone':
        url = RC_SERVICES_BASE_URL + '/toutv/presentation/settings?version=6&device=phone_android'
        headers = {
            'accept-encoding': 'gzip',
            'authorization': f'client-key {client_id}',
            'connection': 'Keep-Alive',
            'user-agent': app_user_agent
        }
        return url, headers
    elif device_type == 'tv':
        url = RC_SERVICES_BASE_URL + '/toutv/presentation/settings?device=androidtv&version=4'
        headers = {
            'Accept-Encoding': 'identity',
            'Accept': '*/*',
            'Authorization': f'Client-Key {client_id}',
            'User-Agent': app_user_agent
        }
        return url, headers


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# SEARCH DB (PHONE)                                                           #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


def get_db_request_data(
    device_type: str,
    client_id: str,
    app_user_agent: str
) -> Tuple[str, Dict[str, str]]:
    if device_type == 'phone':
        url = RC_SERVICES_BASE_URL + '/toutv/presentation/search?version=6&device=phone_android'
        headers = {
            'accept-encoding': 'gzip',
            'authorization': f'client-key {client_id}',
            'connection': 'Keep-Alive',
            'user-agent': app_user_agent
        }
        return url, headers
    elif device_type == 'tv':
        return None, None


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# SEARCH REQUEST (TV)                                                         #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def get_search_request_data(
    device_type: str,
    client_id: str,
    app_user_agent: str,
    query: str
) -> Tuple[str, Dict[str, str]]:
    if device_type == 'phone':
        return None, None
    elif device_type == 'tv':
        url = RC_SERVICES_BASE_URL + '/toutv/presentation/search'
        query_params = {
            'device': 'androidtv',
            'version': '4',
            'term': query.lower()
        }
        headers = {
            'Accept-Encoding': 'identity',
            'Accept': '*/*',
            'Authorization': f'Client-Key {client_id}',
            'User-Agent': app_user_agent
        }
        return f'{url}?{urlencode(query_params)}', headers


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# TITLE                                                                       #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

def get_title_request_data(
    title_id: str,
    device_type: str,
    client_id: str,
    app_user_agent: str
) -> Tuple[str, Dict[str, str]]:
    if device_type == 'phone':
        url = RC_SERVICES_BASE_URL + f'/toutv/presentation/{title_id}?version=6&device=phone_android'
        headers = {
            'accept-encoding': 'gzip',
            'authorization': f'client-key {client_id}',
            'connection': 'Keep-Alive',
            'user-agent': app_user_agent
        }
        return url, headers
    elif device_type == 'tv':
        return None, None
