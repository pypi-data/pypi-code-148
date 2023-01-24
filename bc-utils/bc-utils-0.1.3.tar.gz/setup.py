# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcutils', 'bcutils.tests']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5',
 'numpy>=1.19.4,<1.24.0',
 'pandas>1,<=1.0.5',
 'requests>=2.26,<3.0']

setup_kwargs = {
    'name': 'bc-utils',
    'version': '0.1.3',
    'description': 'Python utility automation scripts for Barchart.com',
    'long_description': '# bc-utils\n\n[Barchart.com](https://www.barchart.com) allows registered users to download historic futures contract prices in CSV \nformat. Individual contracts must be downloaded separately, which is laborious and slow. This script automates the process.\n\n## Quickstart\n\n```\nfrom bcutils.bc_utils import get_barchart_downloads, create_bc_session\n\nCONTRACTS={\n    "AUD":{"code":"A6","cycle":"HMUZ","tick_date":"2009-11-24"},\n    "GOLD": {"code": "GC", "cycle": "GJMQVZ", "tick_date": "2008-05-04"}\n}\n\nsession = create_bc_session(config_obj=dict(\n    barchart_username="user@domain.com",\n    barchart_password = "s3cr3t_321")\n)\n\nget_barchart_downloads(\n    session,\n    contract_map=CONTRACTS,\n    save_directory=\'/home/user/contract_data\',\n    start_year=2020,\n    end_year=2021\n)\n```\n\nThe code above would: \n* for the CME Australian Dollar future, get hourly OHLCV data for the Mar, Jun, Sep and Dec 2020 contracts\n* download in CSV format\n* save with filenames AUD_20200300.csv, AUD_20200600.csv, AUD_20200900.csv, AUD_20201200.csv into the specified directory\n* for COMEX Gold, get Feb, Apr, Jun, Aug, Oct, and Dec data, with filenames like GOLD_20200200.csv etc\n\nFeatures:\n* Designed to be run once a day by a scheduler\n* the script handles skips contracts already downloaded\n* by default gets 120 days of data per contract, override possible per instrument\n* dry run mode to check setup\n* there is logic to switch to daily data when hourly is not available\n* you must be a registered user. Paid subscribers get 100 downloads a day, otherwise 5\n\n',
    'author': 'Andy Geach',
    'author_email': 'andy@bugorfeature.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bug-or-feature/bc-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
