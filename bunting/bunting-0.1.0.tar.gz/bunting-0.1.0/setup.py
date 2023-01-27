# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bunting']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bunting',
    'version': '0.1.0',
    'description': 'SDK for geospatial APIs like OpenStreetMap and Census',
    'long_description': "# Bunting Python SDK\n\nBunting Lab's Python SDK allows you to use the [Bunting Labs geospatial APIs](https://docs.buntinglabs.com/introduction) in your own libraries.\n\n### Installation\n\n```sh\n$ pip install bunting\n```\n\n### Example\n\n```py\nimport BuntingClient from bunting\n\n# Get your API key from https://buntinglabs.com/account/register\nbc = BuntingClient('gK6vkrFQXiU9')\n\n# Download from openstreetmap\nhighways = bc.osm.extract('leisure=park', bbox=(5.976563,52.449314,6.245728,52.562995))\n\n# Get as GeoDataFrame\nhighways.as_gdf()\n```\n",
    'author': 'Brendan Ashworth',
    'author_email': 'brendan@buntinglabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
