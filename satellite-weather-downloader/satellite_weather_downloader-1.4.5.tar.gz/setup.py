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
    'version': '1.4.5',
    'description': 'The modules available in this package are designed to capture and proccess satellite data from Copernicus',
    'long_description': '# Satellite Weather Downloader\n\n| Xarray | Copernicus |\n|:-------------------------:|:-------------------------:|\n|<img width="1604" alt="Xarray" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fxray.readthedocs.io%2Fen%2Fv0.9.0%2F_images%2Fdataset-diagram-logo.png&f=1&nofb=1&ipt=4f24c578ee40cd8ac0634231db6bd24d811fe59658eb2f5f67181f6d720d3f20&ipo=images"> |  <img width="1604" alt="Copernicus" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.eea.europa.eu%2Fabout-us%2Fwho%2Fcopernicus-1%2Fcopernicus-logo%2Fimage&f=1&nofb=1&ipt=56337423b2d920fcf9b4e9dee584e497a5345fc73b20775730740f0ca215fb38&ipo=images">|\n\nSWD is a system for downloading, transforming and analysing Copernicus weather data using Xarray. It consists in two major apps, `satellite_downloader` and `satellite_weather`. `downloader` is responsible for extracting NetCDF4 files from Copernicus API, and the `weather` implements Xarray extensions for transforming and visualizing the files.\n\n## Installation\nThe app is available on PYPI, you can use the package without deploying the containers with the command in your shell:\n``` bash\n$ pip install satellite-weather-downloader\n```\n\n## Requirements\nFor downloading data from Copernicus API, it is required an account. The credentials for your account can be found in Copernicus\' User Page, in the `API key` section. User UID and API Key will be needed in order to request data. Paste them when asked in `satellite_downloader` connection methods.\n\n\n## Notes\nPython Versions = [3.10, 3.11]\n\nVersion 1.X includes only methods for Brazil\'s data format and cities.\n\n## Usage of `copebr` extension\n``` python\nimport satellite_downloader\nimport satellite_weather\n\nfile = satellite_downloader.download_br_netcdf(\'2023-01-01\', \'2023-01-07\')\nbr_dataset = satellite_weather.load_dataset(file)\nrio_dataset = br_dataset.copebr.ds_from_geocode(3304557) # Rio de Janeiro\'s geocode\nrio_dataframe = rio_dataset.to_dataframe()\n```\n\nIt is also possible to create a dataframe directly from the National-wide dataset:\n```\nbr_dataset.copebr.to_dataframe(3304557)\n```\n\nAll Xarray methods are extended when using the `copebr` extension:\n```\nrio_dataset.precip_med.to_array()\nrio_dataset.temp_med.plot()\n```\n',
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
