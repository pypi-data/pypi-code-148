import json
import base64
import pprint
from enum import Enum

import requests


class ProcessStatus(str, Enum):
    ready = "ready"
    pre_processing = "pre-processing"
    pre_processed = "pre-processed"
    processing = "processing"
    processed = "processed"
    post_processing = "post-processing"
    complete = "complete"


class UserRole(str, Enum):
    viewer = "viewer"
    editor = "editor"
    owner = "owner"


class LogFormat(str, Enum):
    ros = "ros"
    mls = "mls"


def output_decorator(func):
    def wrapper(*args, **kwargs):
        if args[0]._pretty:
            return pprint.pprint(func(*args, **kwargs))
        return func(*args, **kwargs)

    return wrapper


class RESTInterface:
    def __init__(self, config):
        self._api_url = config["api_url"]
        self._api_key_id = config["api_key_id"]
        self._api_key_secret = config["api_key_secret"]
        self._pretty = config["pretty"]
        self._dry_run = config["dry_run"]

        auth_header_value = "Bearer " + base64.b64encode(
            bytes(f"{self._api_key_id}:{self._api_key_secret}", "utf-8")
        ).decode("utf-8")

        self._headers = {
            "Authorization": auth_header_value,
            "Content-Type": "application/json",
        }

    def _get_url_param_string(self, args, exclude=[]):
        url_params = ""
        for key, value in args.items():
            if value is not None and key not in ["self"] + exclude:
                if type(value) == dict or type(value) == list:
                    value = json.dumps(value)
                url_params += f"&{key}={value}"
        if len(url_params) > 0:
            url_params = "?" + url_params[1:]
        return url_params

    def _get_payload_data(self, args, exclude=[]):
        payload = {}
        for key, value in args.items():
            if value is not None and key not in ["self"] + exclude:
                payload[key] = value
        return payload

    def _handle_response_data(self, response):
        try:
            response_data = response.json()
        except json.decoder.JSONDecodeError:
            raise Exception(f"Error: {response.text}")
        if response.ok:
            return response_data
        else:
            raise Exception(response_data)

    def _get_resource(self, resource_path):
        if self._dry_run:
            return {}
        r = requests.get(f"{self._api_url}/{resource_path}", headers=self._headers)
        try:
            response_data = r.json()
        except json.decoder.JSONDecodeError:
            raise Exception(f"Error: {r.text}")
        if r.ok:
            return response_data
        else:
            raise Exception(response_data)

    def _create_resource(self, resource_path, data):
        if self._dry_run:
            return {}
        r = requests.post(
            f"{self._api_url}/{resource_path}",
            data=json.dumps(data),
            headers=self._headers,
        )
        return self._handle_response_data(r)

    def _update_resource(self, resource_path, data):
        if self._dry_run:
            return {}
        r = requests.patch(
            f"{self._api_url}/{resource_path}",
            data=json.dumps(data),
            headers=self._headers,
        )
        return self._handle_response_data(r)

    def _delete_resource(self, resource_path):
        if self._dry_run:
            return
        r = requests.delete(f"{self._api_url}/{resource_path}", headers=self._headers)
        return self._handle_response_data(r)
