# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['request_curl']

package_data = \
{'': ['*']}

install_requires = \
['Brotli>=1.0.9,<2.0.0', 'pycurl>=7.45.2,<8.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'request-curl',
    'version': '0.0.1',
    'description': 'A user-friendly wrapper for pycurl that simplifies HTTP requests',
    'long_description': '# Request Curl\n\nA user-friendly wrapper for pycurl that simplifies HTTP requests.\n\n## Installation\nUse the package manager \n[pip](https://pip.pypa.io/en/stable/) \nto install request_curl.\n\n```\npip install request_curl\n```\n\n# Quickstart\nA request_curl session manages cookies, connection pooling, and configurations.\n\nBasic Usage:\n```python\nimport request_curl\ns = request_curl.Session()\ns.get(\'https://httpbin.org/get\') # returns <Response [200]>\ns.request(\'GET\', \'https://httpbin.org/get\') # returns <Response [200]>\n```\n\nUsing a Context Manager\n```python\nimport request_curl\nwith request_curl.Session() as session:\n    session.get(\'https://httpbin.org/get\') # returns <Response [200]>\n```\n\n# Features\n\n## Response Object\n\nThe response object is similar to that of the [requests](https://pypi.org/project/requests/) library.\n\n```python\nimport request_curl\ns = request_curl.Session()\nr = s.get("https://httpbin.org/get")\n\nprint(r) # prints response object\nprint(r.status_code) # prints status code\nprint(r.content) # prints response content in bytes\nprint(r.text) # prints response content as text\nprint(r.json) # prints response content as JSON\nprint(r.url) # prints response URL\nprint(r.headers) # prints response URL\n```\n\n## Proxy Support\nFormat the proxy as a string.\n\n```python\nimport request_curl\ns = request_curl.Session()\n# supports authentication: r = s.get("https://httpbin.org/get", proxies="ip:port:user:password")\nr = s.get("https://httpbin.org/get", proxies="ip:port")\n```\n\n## HTTP2\nHTTP2 is disabled by default.\n\n```python\nimport request_curl\ns = request_curl.Session(http2=True)\nr = s.get("https://httpbin.org/get")\n```\n\n## Cipher Suites\nYou can specify custom cipher suites as an array.\n\n```python\nimport request_curl\n\ncipher_suite = [\n    "AES128-SHA256",\n    "AES256-SHA256",\n    "AES128-GCM-SHA256",\n    "AES256-GCM-SHA384"\n]\ns = request_curl.Session(cipher_suite=cipher_suite)\nr = s.get("https://httpbin.org/get")\n```\n\n## Debug Request\nSet debug to True to print raw input and output headers.\n\n```python\nimport request_curl\ns = request_curl.Session()\nr = s.get("https://httpbin.org/get", debug=True)\n```\n\n## Custom Headers\nSpecify custom headers as a dictionary.\n\n```python\nimport request_curl\ns = request_curl.Session()\nheaders = {\n    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"\n}\nr = s.get("https://httpbin.org/get", headers=headers)\n```\n\n## Data\n\n```python\nimport request_curl\ns = request_curl.Session()\n\n# sending form data\nform_data = {"key": "value"}\nresponse = s.post("https://httpbin.org/post", data=form_data)\n\n# sending json data\njson_data = {"key": "value"}\nresponse = s.post("https://httpbin.org/post", json=json_data)\n```\n\n# Contributing\n\nWe welcome contributions through pull requests. \nBefore making major changes, please open an issue to discuss your intended changes.\nAlso, ensure to update relevant tests.\n\n# License\nEnnis Blank <Ennis.Blank@fau.de>, Mauritz Uphoff <Mauritz.Uphoff@hs-osnabrueck.de>\n\n[MIT](LICENSE)',
    'author': 'Mauritz Uphoff',
    'author_email': 'mauritz.uphoff@hs-osnabrueck.de',
    'maintainer': 'Mauritz Uphoff',
    'maintainer_email': 'None',
    'url': 'https://github.com/Notifysolutions/request_curl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
