# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netport']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'fastapi>=0.85.0,<0.86.0',
 'loguru>=0.6.0,<0.7.0',
 'psutil>=5.9.2,<6.0.0',
 'redis>=4.3.4,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'uvicorn[standard]>=0.18.3,<0.19.0']

entry_points = \
{'console_scripts': ['netport = scripts.cli:main']}

setup_kwargs = {
    'name': 'netport',
    'version': '0.4.0',
    'description': 'Tool for managing resources on a remove machine using openapi',
    'long_description': '# Netport\n\n![Licence](https://badgen.net/pypi/license/netport)\n![Python Versions](https://badgen.net/pypi/python/netport)\n![Pypi Version](https://badgen.net/pypi/v/netport)\n![Code Quality Status](https://github.com/IgalKolihman/netport/actions/workflows/pull_request.yaml/badge.svg)\n\nNetport is a tool for managing single-access resources on the target Unix machine. Netport manages\nthe access to different types of resources on the operating system by not allowing multiple requests\nto the same resource. For example ports, files, processes, network interfaces, and more...\n\n# How it works\n\n```mermaid\nflowchart TD\n    client([Client])\n    server[/Netport Server\\]\n    database[(Database)]\n    resources{{Resources}}\n    ports(Ports)\n    interfaces(Interfaces)\n    fs(File System)\n    proc(System Processes)\n    info(System Info)\n    \n    client <--REST API requests--> server\n    server <--stores server state---> database\n    server <----> resources\n    resources --- ports\n    resources --- interfaces\n    resources --- fs\n    resources --- proc\n    resources --- info\n```\n\n## Framework\n\nNetport runs in a single python process on the target machine. It uses the\n[FastAPI](https://fastapi.tiangolo.com/) framework to make a high performance and easy to use REST\napi server. By using this api, users can easily perform a variety of requests to various resources.\n\nThere are many types of requests that can be made:\n\n* Acquire a free port.\n* Check if file exists\n* Declare that a file is being used\n* Start a process\n* Get a list of already acquired resources\n\nAnd many more...\n\n## Backend Storage\n\nIn order to maintain an active memory of the used resources, Netport communicates with a database.\nThere are 2 types of supported databases that netport uses:\n\n* Redis database\n* Local pythonic database.\n\nBoth databases serve the same purpose for netport, but their inner functionality still a bit\ndifferent, with one draw back for the local database. **The local database doesn\'t save netport\'s\nstate after a shutdown or a reboot**.\n\nThe decision whether to use redis DB or a local one, depends by the user. In case of an unexpected\nshutdown, with redis the state of netport will be stored and on reboot it will continue from where\nit stopped. On the other hand, for much simpler systems this feature might be unnecessary\ncomplicated.\n\n# Installation\n\nMake sure that python is installed on your machine (3.7 and above). Open your terminal and run the\nfollowing command:\n\n```shell\npip install netport\n```\n\n> _It is advised to use a dedicated python virtual environment for netport._\n\n# Developer Installation\n\nInstall poetry by following the instructions [here](https://python-poetry.org/docs/).\n\n1. Clone this repository:\n\n```shell\ngit clone https://github.com/IgalKolihman/netport.git\n```\n\n2. Install the development environment:\n\n```shell\npoetry install --with dev\n```\n\n# Usage\n\nPlease follow the [installation procedure](#installation) to be able to run Netport. After that\nnetport will be available to you as long as you are using it\'s virtual environment.\n\nTo run netport with basic configurations, run:\n\n```shell\nnetport\n```\n\nAfter executing this command, a link will appear in the terminal to the server\'s url. The API\ndocumentation will be available at: _**"http://host_ip:port/docs"**_\n\nFor more advanced information regarding netport execution, run the following command:\n\n```shell\nnetport -h\n```',
    'author': 'Igal Kolihman',
    'author_email': 'igalk.spam@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/IgalKolihman/netport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
