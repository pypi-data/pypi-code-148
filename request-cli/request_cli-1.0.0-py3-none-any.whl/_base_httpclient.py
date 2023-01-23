from yarl import URL
from requests.api import request
from requests.sessions import Session
from requests.hooks import default_hooks
from requests.cookies import cookiejar_from_dict

from ._httpclient_utils import default_headers, TIMEOUT


class BaseHttpClient:

    def __init__(
        self,
        base_url   = None,
        headers    = None,
        timeout    = None,
        cookies    = None,
        auth       = None,
        proxies    = None,
        hooks      = None,
        verify     = True,
        cert       = None,
        stream     = False,
        keep_alive = False,
    ):
        # base_url
        self._base_url = None
        if isinstance(base_url, (str, URL)) or base_url is None:
            base_url = URL(str(base_url))
            if base_url.is_absolute():
                self._base_url = base_url.origin()
        else:
            raise TypeError(f"{self.__class__.__name__}.__init__ 'base_url' type: '{type(base_url).__name__}' 必需是 'str'")

        # headers
        self._headers = default_headers()
        if headers and isinstance(headers, dict):
            self._headers.update(headers)

        # timeout
        self._timeout = TIMEOUT
        if isinstance(timeout, (int, float)):
            if timeout > 0:
                self._timeout = timeout

        # cookies
        if cookies and isinstance(cookies, dict):
            self._cookies = cookiejar_from_dict(cookies)
        else:
            self._cookies = cookiejar_from_dict({})

        # proxies
        self._proxies = {}
        if proxies and isinstance(proxies, dict):
            self._proxies.update(proxies)

        # hooks
        self._hooks = default_hooks()
        if hooks and isinstance(hooks, dict):
            self._proxies.update(hooks)

        # auth
        self._auth = auth
        # verify
        self._verify = verify
        # cert
        self._cert = cert
        # stream
        self._stream = stream
        # http client
        self._keep_alive = keep_alive
        self._request = self._gen_request()

    def _gen_request(self):
        self._session = Session()
        if self._keep_alive:
            return self._session.request
        return request

    def build_url(self, url):
        if not isinstance(url, (str, URL)):
            raise TypeError(f"'url' type: '{type(url).__name__}' 必需是 'str'")
        url = URL(str(url))
        if not self._base_url or url.is_absolute():
            return url
        return self._base_url.join(url)

    def close(self):
        self._session.close()
        if self._keep_alive:
            self._request = self._gen_request()