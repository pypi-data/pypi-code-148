# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['usermgr', 'usermgr.providers']

package_data = \
{'': ['*']}

extras_require = \
{'cognito': ['boto3>=1.26.54,<2.0.0']}

setup_kwargs = {
    'name': 'usermgr',
    'version': '0.0.2',
    'description': '',
    'long_description': '# User Management API\n\n## Memo\n\n* unittest\n\n  * prepare .env file\n\n```\nAWS_ACCESS_KEY_ID=xxx\nAWS_SECRET_ACCESS_KEY=xxx\nor\nAWS_PROFILE=xxx\n\nUSER_POOL_ID=xxx\nCLIENT_ID=xxx\n```\n\n  * run unittest\n\n```\npoetry run dotenv run python -m unittest discover\n```\n\n* build\n\n```\npoetry build\n```\n\n* public\n\n```\npoetry publish\n```\n\n* Install for development\n\n```\npoetry install -E cognito\n```\n',
    'author': 'tamuto',
    'author_email': 'tamuto@infodb.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tamuto/usermgr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
