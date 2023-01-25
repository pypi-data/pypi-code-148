# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umipy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'pydantic>=1.10.4,<2.0.0']

setup_kwargs = {
    'name': 'umipy',
    'version': '0.0.1',
    'description': '',
    'long_description': '# UMIPY\n\nAsynchronous python api wrapper for [umi-api](https://github.com/RoyFractal/umi-api)\n\nImplements all methods from umi-api.\n\nNow there are the following methods:\n- /get_balance\n- /get_transactions\n- /generate_wallet\n- /send\n- /sign_message\n- /restore_wallet\n\n\n### Install\n\nfor stable version\n\n`pip install umipy`\n\nfor dev version\n\n`pip install https://github.com/RoyFractal/PyUmi/archive/master.zip` \n\n\n### Usage\n\nYou can find more examples - [examples/](examples/)\n\n#### simple getting a address data\n\n```python3\nimport asyncio\n\nfrom umipy import UmiPy\n\n\nasync def main():\n    umi = UmiPy()\n    balance = await umi.get_balance(\n        "umi17ymaed9h9hq7s5pc2f5fhmlzpmsk3qtc6g2cgm360zysz0uvq44qnxlsuz"\n    )\n    print(balance)\n\n    trans = await umi.get_transactions(\n        "umi17ymaed9h9hq7s5pc2f5fhmlzpmsk3qtc6g2cgm360zysz0uvq44qnxlsuz"\n    )\n    print(trans)\n\n    await umi.close()\n\n\nasyncio.run(main())\n```\n',
    'author': 'kesha1225',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
