# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['satellite_downloader',
 'satellite_downloader.utils',
 'satellite_weather',
 'satellite_weather.utils']

package_data = \
{'': ['*']}

install_requires = \
['MetPy>=1.3.1,<2.0.0',
 'SQLAlchemy>=1.4.41,<2.0.0',
 'amqp>=5.1.1,<6.0.0',
 'cdsapi>=0.5.1,<0.6.0',
 'celery>=5.2.7,<6.0.0',
 'flower>=1.2.0,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'netCDF4>=1.6.1,<2.0.0',
 'numpy>=1.23.3,<2.0.0',
 'pandas>=1.5.0,<2.0.0',
 'psycopg2-binary>=2.9.4,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'satellite-weather-downloader',
    'version': '1.4.3',
    'description': 'The modules available in this package are designed to capture and proccess satellite data from Copernicus',
    'long_description': '<!-- satellite_weather_downloader -->\n',
    'author': 'Luã Bida Vacaro',
    'author_email': 'luabidaa@gmail.com',
    'maintainer': 'Luã Bida Vacaro',
    'maintainer_email': 'luabidaa@gmail.com',
    'url': 'https://github.com/osl-incubator/satellite-weather-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4',
}


setup(**setup_kwargs)
