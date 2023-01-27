import json
import logging
from typing import Any, Callable, Dict, Mapping, Optional, Type, Union

import requests
from requests import HTTPError, Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from the_spymaster_util.http.defs import CONTEXT_HEADER_KEY, ErrorTypes
from the_spymaster_util.http.errors import DEFAULT_ERRORS
from the_spymaster_util.logger import wrap
from the_spymaster_util.measure_time import MeasureTime
from the_spymaster_util.strings import camel_to_const, get_class_name

log = logging.getLogger(__name__)

DEFAULT_RETRY_STRATEGY = Retry(
    raise_on_status=False,
    total=2,
    backoff_factor=0.3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "OPTIONS", "GET", "POST", "PUT", "DELETE"],
)


class BaseHttpClient:
    def __init__(self, base_url: str, retry_strategy: Optional[Retry] = DEFAULT_RETRY_STRATEGY):
        self.base_url = base_url
        self.session = requests.Session()
        self.set_retry_strategy(retry_strategy)
        log.debug(f"{self.__class__.__name__} client using base url {wrap(self.base_url)}")

    def set_retry_strategy(self, retry_strategy: Optional[Retry]):
        retry_adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", retry_adapter)
        self.session.mount("https://", retry_adapter)

    def _http_call(
        self,
        endpoint: str,
        method: Callable,
        parse: bool = True,
        error_types: Optional[ErrorTypes] = DEFAULT_ERRORS,
        **kwargs,
    ) -> Union[dict, Response]:
        url = f"{self.base_url}/{endpoint}"
        headers = kwargs.pop("headers", None) or {}
        data = kwargs.get("data")
        log_context = getattr(log, "context", None)
        if log_context:
            headers[CONTEXT_HEADER_KEY] = json.dumps(log_context)
        log_http_data = kwargs.pop("log_http_data", True)
        method_name = method.__name__.upper()
        _log_request(method=method_name, url=url, data=data, headers=headers, log_http_data=log_http_data)
        with MeasureTime() as mt:  # pylint: disable=invalid-name
            response = method(url, headers=headers, **kwargs)
        _log_response(method=method_name, url=url, response=response, duration=mt.delta, log_http_data=log_http_data)
        _validate(response=response, error_types=error_types)
        if parse:
            return response.json()
        return response

    def _get(
        self,
        endpoint: str,
        data: dict,
        error_types: Optional[ErrorTypes] = DEFAULT_ERRORS,
        **kwargs,
    ) -> Union[dict, Response]:
        return self._http_call(
            endpoint=endpoint,
            method=self.session.get,
            params=data,
            error_types=error_types,
            **kwargs,
        )

    def _post(
        self,
        endpoint: str,
        data: dict,
        error_types: Optional[ErrorTypes] = DEFAULT_ERRORS,
        **kwargs,
    ) -> Union[dict, Response]:
        return self._http_call(
            endpoint=endpoint,
            method=self.session.post,
            json=data,
            error_types=error_types,
            **kwargs,
        )  # type: ignore


def _validate(response: Response, error_types: Optional[ErrorTypes] = None):
    try:
        response.raise_for_status()
    except HTTPError as http_error:
        _raise_custom_error(response=response, http_error=http_error, error_types=error_types)


def _raise_custom_error(response: Response, http_error: HTTPError, error_types: Optional[ErrorTypes] = None):
    if not error_types:
        raise http_error
    try:
        data = response.json()
    except Exception:  # noqa
        raise http_error  # pylint: disable=raise-missing-from
    error_code = data.pop("error_code", None)
    if not error_code:
        raise http_error
    error_code_mapping = _get_error_code_mapping(error_types=error_types)
    error_class = error_code_mapping.get(error_code)
    if not error_class:
        raise http_error
    try:
        parsed_error = error_class(**data)  # type: ignore
    except Exception as error_init_error:
        log.warning(f"Error code {error_code} exists, but failed to init: {error_init_error}")
        raise http_error  # pylint: disable=raise-missing-from
    raise parsed_error from http_error


def _log_request(method: str, url: str, data: Optional[dict], headers: Optional[dict], log_http_data: bool = True):
    extra: Dict[str, Any] = {"method": method, "url": url}
    if log_http_data:
        extra["data"] = data
        extra["headers"] = headers
    log.debug(f"Sending: {wrap(method)} to {wrap(url)}", extra=extra)


def _log_response(method: str, url: str, response: Response, duration: float, log_http_data: bool = True):
    extra = {"method": method, "url": url, "status_code": response.status_code, "duration": duration}
    if log_http_data:
        try:
            data = response.json()
        except Exception:  # noqa
            data = str(response.content)
        extra["data"] = data
    log.debug(f"Received: {wrap(response.status_code)}", extra=extra)


def extract_context(headers: Mapping[str, Any]) -> dict:
    try:
        context_json = headers.get(CONTEXT_HEADER_KEY)
        if not context_json:
            return {}
        return json.loads(context_json)
    except Exception as e:  # pylint: disable=invalid-name
        log.debug(f"Failed to extract context from headers: {e}")
        return {}


def get_error_code(exception: Union[Exception, Type[Exception]]) -> str:
    error_code = getattr(exception, "error_code", None)
    if not error_code:
        error_code = get_class_name(exception)
    return camel_to_const(error_code)


def _get_error_code_mapping(error_types: ErrorTypes) -> Dict[str, Type[Exception]]:
    return {get_error_code(error): error for error in error_types}
