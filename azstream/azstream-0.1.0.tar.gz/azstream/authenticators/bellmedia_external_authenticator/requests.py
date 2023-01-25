from typing import Dict
from base64 import b64encode
from urllib.parse import urlencode
from .consts import LOGIN_URL,          LOGIN_BODY,       LOGIN_HEADERS,\
                    REFRESH_URL,        REFRESH_BODY,     REFRESH_HEADERS,\
                    MAGIC_GENERATE_URL,                   MAGIC_GENERATE_HEADERS,\
                    MAGIC_LOGIN_URL,    MAGIC_LOGIN_BODY, MAGIC_LOGIN_HEADERS,\
                    PROFILE_URL,                          PROFILE_HEADERS,\
                    CAPTCHA_URL
from copy import deepcopy


def get_captcha_request_data() -> str:
    return CAPTCHA_URL

def get_login_request_data(
    username: str, 
    password: str, 
    captcha: str,
    web_credentials: tuple[str, str],
    app_headers_tag: str,
    user_agent: str
) -> tuple[str, str, Dict[str, str]]:
    url = LOGIN_URL
    body_dict = deepcopy(LOGIN_BODY)
    body_dict['username'] = body_dict['username'].format(username=username)
    body_dict['password'] = body_dict['password'].format(password=password)
    body_dict['recaptcha_token'] = body_dict['recaptcha_token'].format(captcha=captcha)
    body = urlencode(body_dict)
    headers = deepcopy(LOGIN_HEADERS)
    headers['authorization']    = headers['authorization'].format(app_token=generate_basic_token(web_credentials))
    headers['x-requested-with'] = headers['x-requested-with'].format(app_headers_tag=app_headers_tag)
    headers['user-agent'] = headers['user-agent'].format(user_agent=user_agent)
    return url, body, headers

def get_refresh_request_data(
    refresh_token: str, 
    profile_id: str,
    app_credentials: tuple[str, str]
) -> tuple[str, str, Dict[str, str]]:
    url = REFRESH_URL
    body_dict = deepcopy(REFRESH_BODY)
    body_dict['refresh_token'] = body_dict['refresh_token'].format(refresh_token=refresh_token)
    body_dict['profile_id'] = body_dict['profile_id'].format(profile_id=profile_id)
    body = urlencode(body_dict)
    headers = deepcopy(REFRESH_HEADERS)
    headers['authorization']    = headers['authorization'].format(app_token=generate_basic_token(app_credentials))
    return url, body, headers

def get_magic_generate_request_data(
    login_token: str,
    app_headers_tag: str,
    user_agent: str
) -> tuple[str, Dict[str, str]]:
    url = MAGIC_GENERATE_URL
    headers = deepcopy(MAGIC_GENERATE_HEADERS)
    headers['authorization']    = headers['authorization'].format(login_token=login_token)
    headers['x-requested-with'] = headers['x-requested-with'].format(app_headers_tag=app_headers_tag)
    headers['user-agent'] = headers['user-agent'].format(user_agent=user_agent)
    return url, headers
    
def get_magic_login_request_data(
    magic_token: str,
    app_credentials: tuple[str, str]
) -> tuple[str, str, Dict[str, str]]:
    url = MAGIC_LOGIN_URL
    body_dict = deepcopy(MAGIC_LOGIN_BODY)
    body_dict['magic_link_token'] = body_dict['magic_link_token'].format(magic_token=magic_token)
    body = urlencode(body_dict)
    headers = deepcopy(MAGIC_LOGIN_HEADERS)
    headers['authorization'] = headers['authorization'].format(app_token=generate_basic_token(app_credentials))
    return url, body, headers

def get_profile_request_data(
    access_token: str
) -> tuple[str, Dict[str, str]]:
    url = PROFILE_URL
    headers = deepcopy(PROFILE_HEADERS)
    headers['authorization'] = headers['authorization'].format(access_token=access_token)
    return url, headers

def generate_basic_token(credentials: tuple[str, str]) -> str:
    return b64encode(f'{credentials[0]}:{credentials[1]}'.encode()).decode()