""" requests 模块封装 """
import warnings
from time import sleep
from functools import wraps

import requests.exceptions
from requests.utils import CaseInsensitiveDict

from ._base_httpclient import BaseHttpClient
from ._httpclient_utils import default_headers



def complete_request(function):

    @wraps(function)
    def wrapper(*args, **kwargs):
        retry_sleep = 0.5
        retry_max   = 10
        retry_dict  = {}

        while True:
            try:
                response = function(*args, **kwargs)
                # 状态码判断
                status = response.status_code
                if str(status).startswith("4"):
                    raise requests.exceptions.InvalidURL(
                        f"url: '{response.url}', invalid status code: '{status}'"
                    )

                # 捕获异常请求 并重试 达到最大重试次数返回
                if status != 200:
                    warnings.warn(f"\033[33murl: '{response.url}', status_code: '{status}'\033[0m")
                    retry_dict.setdefault(status, 0)
                    retry_dict[status] += 1
                    if retry_dict[status] >= retry_max:
                        warnings.warn(f"\033[33mstatus_code: '{status}' 重试达到最大值 '{retry_max}', 已返回 response'\033[0m")
                        break
                    sleep(retry_sleep)
                    continue
                break

            # 捕获超时 并 重新请求
            except requests.exceptions.Timeout as error:
                reason = error.args[0].reason.args[1]
                warnings.warn(f"{reason}: {error.request.url}")
                sleep(retry_sleep)

            # 捕获连接异常
            except requests.exceptions.ConnectionError as error:
                reason = error.args[0].reason.args[0]
                reason = reason.split(":", 1)[-1].strip()
                warnings.warn(f"{reason}: '{error.request.url}'")
                sleep(retry_sleep)

        # resp.encoding = resp.apparent_encoding
        return response
    return wrapper



class HttpClient(BaseHttpClient):

    @complete_request
    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
        ua=None
    ):
        # headers
        if not isinstance(headers, dict):
            headers = self._headers
        else:
            headers = CaseInsensitiveDict({**self._headers, **headers})
        # 更新UserAgent
        if ua:
            if isinstance(ua, (str)):
                headers.update(default_headers(ua))
            elif isinstance(ua, (list, tuple, set)):
                headers.update(default_headers(*ua))
            elif isinstance(ua, dict):
                headers.update(**ua)
        # timeout
        if not (isinstance(timeout, (int, float)) and timeout > 0):
            timeout = self._timeout

        return self._request(
            method=method,
            url=self.build_url(url),
            params=params,
            data=data,
            headers=headers,
            cookies=cookies or self._cookies,
            files=files,
            auth=auth or self._auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies or self._proxies,
            hooks=hooks or self._hooks,
            stream=stream or self._stream,
            verify=verify or self._verify,
            cert=cert or self._cert,
            json=json
        )


    def get(self, url, allow_redirects=True, **kwargs):
        # kwargs["allow_redirects"] = allow_redirects
        return self.request("GET", url, allow_redirects=allow_redirects, **kwargs)

    def post(self, url, data=None, json=None, allow_redirects=True, **kwargs):
        # kwargs["allow_redirects"] = allow_redirects
        return self.request("POST", url, data=data, json=json, allow_redirects=allow_redirects, **kwargs)

    def head(self, url, allow_redirects=False, **kwargs):
        # kwargs["allow_redirects"] = allow_redirects
        return self.request("HEAD", url, allow_redirects=allow_redirects, **kwargs)

    def options(self, url, allow_redirects=True, **kwargs):
        # kwargs["allow_redirects"] = allow_redirects
        return self.request("OPTIONS", url, allow_redirects=allow_redirects, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data=data, **kwargs)
