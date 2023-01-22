# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jackett_indexerarr']

package_data = \
{'': ['*']}

install_requires = \
['requests', 'typer']

entry_points = \
{'console_scripts': ['jackett-indexerarr = jackett_indexerarr.cli:app']}

setup_kwargs = {
    'name': 'jackett-indexerarr',
    'version': '0.15',
    'description': '',
    'long_description': '# jackett indexarr\n\nSets up radarr, sonarr, readarr & lidarr with the configured trackers in jackett\n\nJackett connection setup\n```\nexport jackett_cookie="get the cookie from chrome session"\nexport jackett_endpoint="http://192.168.0.30:9117"\nexport jackett_api_key="dddddddddddddddddddddddddddddddddddddddddd"\n```\n\nDefine where sonarr, radarr & lidarr dbs are\n```\nexport sonarr_db="/home/to/sonarr/sonarr.db"\nexport radarr_db="/home/to/radarr/radarr.db"\nexport lidarr_db="/home/to/lidarr/lidarr.db"\n```\n\nExecute it\n```\npip install jackett-indexerarr\njackett-indexerarr\n```',
    'author': 'David O Neill',
    'author_email': 'dmz.oneill@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dmzoneill/jackett-indexerarr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
