"""
Copyright (C) 2022 Corsair M360, Inc - All Rights Reserved.
Unauthorized copying of this file, via any medium is strictly prohibited.
Proprietary and confidential.
"""

import json
import time
import logging
import requests

from m360 import constants

_logger = logging.getLogger(__name__)

def request(*, url, method="get", headers=None, query=None, body=None, is_json=False, verify=False):
    _logger.debug("Executing request: " + method + " " + url)
    if is_json:
        headers = headers if headers is not None else {}
        headers["Content-Type"] = "application/json"
    return requests.request(url=url, method=method, headers=headers, params=query, json=body, verify=verify)

def retry_request(*, url, method="get", headers=None, query=None, body=None, is_json=False, verify=False, retries=0,
                  retry_delay=constants.DEFAULT_RETRY_DELAY_SEC):
    counter = 0
    errors = ""
    ok = False
    main_res = None

    # make request with retry strategy
    while not ok:
        try:
            main_res = request(url=url, method=method, headers=headers, query=query, body=body, is_json=is_json,
                               verify=verify)
            res = main_res.json()
            # _logger.debug("Response: " + str(res))
            counter += 1
            # response is: { result: boolean, errors?: {}, data?: any }
            if res and isinstance(res, dict) and "result" in res:
                if res.get("result") is False or res.get("errors"):
                    if isinstance(res.get("errors"), dict):
                        for err in res.get("errors").values():
                            errors += err.get("message") + "\n"
                    if counter <= retries:
                        time.sleep(retry_delay)
                    else:
                        break
                else:
                    ok = True
                    break
            else:
                ok = True
                break
        except Exception as e:
            _logger.error(e)
            errors += str(e) + "\n"
            counter += 1
            if counter <= retries:
                time.sleep(retry_delay)
            else:
                break
    # return
    if ok:
        _logger.debug("Successfully called " + method.upper() + " " + url)
        return main_res
    else:
        _logger.error("Error(s) while calling " + method.upper() + " " + url)
        raise Exception(errors)

def json_file_to_dict(filepath):
    """
    Loads the file at the specified path and parses the JSON into a dict
    @param filepath  {str}  Path to a JSON file
    @returns {dict} The resulting dict
    """
    if not filepath or type(filepath) is not str or not filepath.strip():
        _logger.error("Invalid file path")
        raise Exception("Invalid file path")

    try:
        with open(filepath, mode="r", encoding="utf8") as f:
            data = f.read()
        data = json.loads(data)
        return data
    except Exception as e:
        _logger.error(e)
        raise e

def to_json(obj):
    return json.dumps(obj, separators=(",", ":"))

def from_json(text):
    return json.loads(text)

def get_req_headers(req):
    if hasattr(req, "headers"):
        return req.headers
    if hasattr(req, "META"):
        return req.META
    return {}

def is_array(obj):
    return isinstance(obj, list)

def is_dict(obj):
    return isinstance(obj, dict)

def is_string(obj):
    return isinstance(obj, str)

def is_iterable(obj):
    try:
        iterator = iter(obj)
    except TypeError:
        return False
    else:
        return True

def build_object_from_path(obj, path, value):
    paths = path.split(".")
    last = paths.pop()
    ref = obj
    for p in paths:
        if not ref.get(p):
            ref[p] = {}
        ref = ref[p]
    ref[last] = value

def remove_object_from_path(obj, path):
    paths = path.split(".")
    last = paths.pop()
    ref = obj
    for p in paths:
        if ref.get(p):
            ref = ref[p]
        else:
            return
    if ref.get(last):
        del ref[last]
