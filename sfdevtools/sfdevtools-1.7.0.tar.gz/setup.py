# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfdevtools',
 'sfdevtools.app',
 'sfdevtools.devTools',
 'sfdevtools.observability',
 'sfdevtools.observability.logging_json',
 'sfdevtools.observability.logstash']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sfdevtools',
    'version': '1.7.0',
    'description': '',
    'long_description': '## How to publish to pypi\n```bash\n# set up pypi token\npoetry config pypi-token.pypi my-token\n\n# build the project\npoetry build\n\n# publish the project\npoetry publish\n\n# DONE\n```\n\n## Demo example\n### Double check lock for singleton\n```python\nimport sfdevtools.observability.log_helper as lh\nimport logging\nlogger = lh.init_logger(logger_name="sfdevtools_logger", is_json_output=False)\n# create class X\nclass X(SDC):\n    pass\n\n# create class Y\nclass Y(SDC):\n    pass\n\nA1, A2 = X.instance(), X.instance()\nB1, B2 = Y.instance(), Y.instance()\n\nassert A1 is not B1\nassert A1 is A2\nassert B1 is B2\n\nlogger.info(\'A1 : {}\'.format(A1))\nlogger.info(\'A2 : {}\'.format(A2))\nlogger.info(\'B1 : {}\'.format(B1))\nlogger.info(\'B2 : {}\'.format(B2))\n```\n\n### Send log to logstash\n```python\nlogger = lh.init_logger(logger_name="connection_tester_logger"\n                        , is_json_output=False\n                        , is_print_to_console=True\n                        , is_print_to_logstash=True\n                        , logstash_host="<the host name>"\n                        , logstash_port=5960\n                        , logstash_user_tags=["Test001", "Test002"])\nlogger.info("Test Message from test")\nlogger.error("Test Message from test")\nlogger.warning("Test Message from test")\n```\n',
    'author': 'SulfredLee',
    'author_email': 'sflee1112@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
