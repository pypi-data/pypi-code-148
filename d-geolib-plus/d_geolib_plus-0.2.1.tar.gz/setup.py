# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geolib_plus',
 'geolib_plus.bro_xml_cpt',
 'geolib_plus.cpt_utils',
 'geolib_plus.gef_cpt',
 'geolib_plus.robertson_cpt_interpretation',
 'geolib_plus.shm']

package_data = \
{'': ['*'],
 'geolib_plus.cpt_utils': ['resources/*'],
 'geolib_plus.gef_cpt': ['resources/*'],
 'geolib_plus.robertson_cpt_interpretation': ['resources/*'],
 'geolib_plus.shm': ['resources/*']}

install_requires = \
['d-geolib>=0.2.3,<0.3.0',
 'lxml>=4.7,<5.0',
 'matplotlib>=3.4,<4.0',
 'more-itertools>=8.6,<9.0',
 'netCDF4>=1.5,<2.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.4,<2.0',
 'pydantic>=1,<2',
 'pyproj>=3.3,<4.0',
 'pyshp>=2.1,<3.0',
 'requests>=2.26,<3.0',
 'scipy>=1.6,<2.0',
 'shapely==2.0.0',
 'tqdm>=4,<5']

setup_kwargs = {
    'name': 'd-geolib-plus',
    'version': '0.2.1',
    'description': 'GEOLib+ components',
    'long_description': 'GEOLib+\n=============================\n\nGEOLib+ is a Python package to read, interprent and plot cpt files.\nThe package can also be used to get soil parameters for constitutive models.\n\nInstallation\n------------\n\nInstall GEOLib+ with:\n\n.. code-block:: bash\n\n    $ pip install d-geolib-plus\n\n\nRequirements\n------------\n\nTo install the required dependencies to run GEOLib+ code, run:\n\n.. code-block:: bash\n\n    $ pip install -r requirements\n\nOr, when having poetry installed (you should):\n\n.. code-block:: bash\n\n    $ poetry install\n\n\nTesting & Development\n---------------------\n\nMake sure to have the server dependencies installed: \n\n.. code-block:: bash\n\n    $ poetry install -E server\n\nIn order to run the testcode, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ pytest\n\nor, in case of using Poetry\n\n.. code-block:: bash\n\n    $ poetry run pytest\n\nRunning flake8, mypy is also recommended. For mypy use:\n\n.. code-block:: bash\n\n    $ mypy --config-file pyproject.toml geolib\n\n\nDocumentation\n-------------\n\nIn order to run the documentation, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ cd docs\n    $ sphinx-build . build -b html -c .\n\n\nThe documentation is now in the `build` subfolder, where you can open \nthe `index.html` in your browser.\n\nBuild wheel\n-----------\n\nTo build a distributable wheel package, run:\n\n.. code-block:: bash\n\n    $ poetry build\n\nThe distributable packages are now built in the `dist` subfolder.',
    'author': 'Maarten Pronk',
    'author_email': 'git@evetion.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://deltares.github.io/geolib-plus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
