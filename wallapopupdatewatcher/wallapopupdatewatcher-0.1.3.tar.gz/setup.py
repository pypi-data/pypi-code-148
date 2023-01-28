# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wallapopupdatewatcher']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0']

setup_kwargs = {
    'name': 'wallapopupdatewatcher',
    'version': '0.1.3',
    'description': 'A library to watch for new items at wallapop.es',
    'long_description': '# Wallapop update notifier\n\n### This package can be used to provide updates when new products appear on Wallapop. Install it just by using:<br><br>\n`pip install wallapopUpdateWatcher`\n### Basic usage example\n```python\nfrom wallapopUpdateWatcher import updateWatcher,Query,Producto\nimport asyncio\nasync def callback(q: Query, l: list[Producto]):\n    for prod in l:\n        print(prod.msg())\n\n\nasync def main():\n    watcher = updateWatcher(callback)\n    await watcher.create("Iphone",strategy="price", min_max_sale_price = (15,30))\n    # this creates a search for the product "Iphone"\n    # between 15€ and 30€. \n\n    while True:\n        await watcher.checkOperation()\n        await asyncio.sleep(5)\n\nasyncio.run(main())\n```\n\n## Strategies:\nStrategies are what decides if a product that has already appeared sometime is going to be notified. There are 3 strategies:\n- Price:\nThis strategy only adds the product if its price has changed. It is the **default** strategy.\n\n- New:\nThis strategy only notifies new products.\n\n- Any:\nThis strategy notifies any product, even if it has already been notified.',
    'author': 'Adair-GA',
    'author_email': 'adairyves@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Adair-GA/wallapopUpdateWatcher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
