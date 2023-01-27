# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['momento',
 'momento.auth',
 'momento.config',
 'momento.config.transport',
 'momento.errors',
 'momento.internal',
 'momento.internal._utilities',
 'momento.internal.aio',
 'momento.internal.common',
 'momento.internal.synchronous',
 'momento.requests',
 'momento.responses',
 'momento.responses.control',
 'momento.responses.scalar_data']

package_data = \
{'': ['*']}

install_requires = \
['grpcio==1.50.0', 'momento-wire-types==0.31.1', 'pyjwt==2.4.0']

setup_kwargs = {
    'name': 'momento',
    'version': '0.19.0',
    'description': 'SDK for Momento',
    'long_description': '<head>\n  <meta name="Momento Python Client Library Documentation" content="Python client software development kit for Momento Serverless Cache">\n</head>\n<img src="https://docs.momentohq.com/img/logo.svg" alt="logo" width="400"/>\n\n[![project status](https://momentohq.github.io/standards-and-practices/badges/project-status-official.svg)](https://github.com/momentohq/standards-and-practices/blob/main/docs/momento-on-github.md)\n[![project stability](https://momentohq.github.io/standards-and-practices/badges/project-stability-alpha.svg)](https://github.com/momentohq/standards-and-practices/blob/main/docs/momento-on-github.md) \n\n# Momento Python Client Library\n\n\nPython client SDK for Momento Serverless Cache: a fast, simple, pay-as-you-go caching solution without\nany of the operational overhead required by traditional caching solutions!\n\n\n\n## Getting Started :running:\n\n### Requirements\n\n- [Python 3.7](https://www.python.org/downloads/) or above is required\n- A Momento Auth Token is required, you can generate one using the [Momento CLI](https://github.com/momentohq/momento-cli)\n\n### Examples\n\nReady to dive right in? Just check out the [examples](./examples/README.md) directory for complete, working examples of\nhow to use the SDK.\n\n### Installation\n\nThe [Momento SDK is available on PyPi](https://pypi.org/project/momento/).  To install via pip:\n\n```bash\npip install momento\n```\n\n### Usage\n\nHere is a quickstart you can use in your own project:\n\n```python\nimport logging\nimport os\n\nfrom example_utils.example_logging import initialize_logging\n\nimport momento.errors as errors\nimport momento.simple_cache_client as scc\n\n_MOMENTO_AUTH_TOKEN = os.getenv("MOMENTO_AUTH_TOKEN")\n_CACHE_NAME = "cache"\n_ITEM_DEFAULT_TTL_SECONDS = 60\n_KEY = "MyKey"\n_VALUE = "MyValue"\n\n_logger = logging.getLogger("momento-example")\n\n\ndef _print_start_banner() -> None:\n    _logger.info("******************************************************************")\n    _logger.info("*                      Momento Example Start                     *")\n    _logger.info("******************************************************************")\n\n\ndef _print_end_banner() -> None:\n    _logger.info("******************************************************************")\n    _logger.info("*                       Momento Example End                      *")\n    _logger.info("******************************************************************")\n\n\ndef _create_cache(cache_client: scc.SimpleCacheClient, cache_name: str) -> None:\n    try:\n        cache_client.create_cache(cache_name)\n    except errors.AlreadyExistsError:\n        _logger.info(f"Cache with name: {cache_name!r} already exists.")\n\n\ndef _list_caches(cache_client: scc.SimpleCacheClient) -> None:\n    _logger.info("Listing caches:")\n    list_cache_result = cache_client.list_caches()\n    while True:\n        for cache_info in list_cache_result.caches():\n            _logger.info(f"- {cache_info.name()!r}")\n        next_token = list_cache_result.next_token()\n        if next_token is None:\n            break\n        list_cache_result = cache_client.list_caches(next_token)\n    _logger.info("")\n\n\nif __name__ == "__main__":\n    initialize_logging()\n    _print_start_banner()\n    with scc.SimpleCacheClient(_MOMENTO_AUTH_TOKEN, _ITEM_DEFAULT_TTL_SECONDS) as cache_client:\n        _create_cache(cache_client, _CACHE_NAME)\n        _list_caches(cache_client)\n\n        _logger.info(f"Setting Key: {_KEY!r} Value: {_VALUE!r}")\n        cache_client.set(_CACHE_NAME, _KEY, _VALUE)\n\n        _logger.info(f"Getting Key: {_KEY!r}")\n        get_resp = cache_client.get(_CACHE_NAME, _KEY)\n        _logger.info(f"Look up resulted in a : {str(get_resp.status())}")\n        _logger.info(f"Looked up Value: {str(get_resp.value())!r}")\n    _print_end_banner()\n\n```\n\nNote that the above code requires an environment variable named MOMENTO_AUTH_TOKEN which must\nbe set to a valid [Momento authentication token](https://docs.momentohq.com/docs/getting-started#obtain-an-auth-token).\n\n### Error Handling\n\nComing Soon!\n\n### Tuning\n\nComing Soon!\n\n----------------------------------------------------------------------------------------\nFor more info, visit our website at [https://gomomento.com](https://gomomento.com)!\n',
    'author': 'Momento',
    'author_email': 'hello@momentohq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gomomento.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
