"""Networking helpers
"""
import json
from json import JSONDecodeError
import requests

import re

from eze.utils.error import EzeNetworkingError
from eze.utils.log import log_debug


def request_json(url: str, *, data=None, headers=None, method="GET") -> dict:
    """
    requests a url and convert return into json

    :raises EzeNetworkingError: on networking error or json decoding error"""
    contents: str = request(url, data=data, headers=headers, method=method)
    try:
        return json.loads(contents)
    except JSONDecodeError as error:
        raise EzeNetworkingError(f"Error in JSON response '{url}', {contents} ({error})")


def request(url: str, *, data=None, headers=None, method="GET") -> str:
    """
    requests a url and returns string

    :raises EzeNetworkingError: on networking error
    """
    response: requests.Response = request_raw(url, data=data, headers=headers, method=method)
    return response.text


def request_raw(url: str, *, data=None, headers=None, method="GET") -> requests.Response:
    """
    requests a url and returns string

    :raises EzeNetworkingError: on networking error
    """
    log_debug(f"calling url '{url}'")
    if not headers:
        headers = {}
    try:
        response: requests.Response = requests.request(method, url, data=data, headers=headers)
        return response
    except requests.exceptions.RequestException as error:
        raise EzeNetworkingError(f"Error accessing url '{url}', Error: {error}")


def spine_case_url(url: str) -> str:
    """convert url into spine case, file name safe version"""
    cleaned_url = re.sub("^https?:?[/][/]", "", url)
    cleaned_url = re.sub("^[a-zA-Z0-9.]+@[a-zA-Z0-9.]+:", "", cleaned_url)
    cleaned_url = re.sub("\\.[a-z]{,4}$", "", cleaned_url)
    cleaned_url = re.sub("[^a-zA-Z0-9]+", "-", cleaned_url)
    cleaned_url = re.sub("[-]+", "-", cleaned_url)
    return cleaned_url
