# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['param_sweeps']

package_data = \
{'': ['*']}

install_requires = \
['geoh5py>=0.6.0,<0.7.0', 'numpy>=1.21.5,<2.0.0']

setup_kwargs = {
    'name': 'param-sweeps',
    'version': '0.1.4',
    'description': 'Parameter sweeper for ui.json powered applications',
    'long_description': '# Param-sweeps\n\nA Parameter sweeper for applications driven by ui.json files\n\nThis package contains two main modules.  One is for generating sweep\nfiles, and the other is to run a sweep over some number of parameters\nin a driver application.\n\n### Basic Usage\n\nTo generate a sweep file from a ui.json file for an existing\napplication, use the following command:\n\n```bash\npython -m param_sweeps.generate some_file.ui.json\n```\n\nThis will create a new `some_file_sweep.ui.json` file that may be run\nwith:\n\n```bash\npython -m param_sweeps.driver some_file_sweep.ui.json\n```\n\nBy default, this would execute a single run of the original parameters.\nTo design a sweep, simply drag the `some_file_sweep.ui.json` file into\nthe [Geoscience ANALYST Pro](https://mirageoscience.com/mining-industry-software/geoscience-analyst-pro/)\nsession that produced the original file and select start, end, and number\nof samples values for parameters that you would like to sweep.\n\n\nTo organize the output, param-sweeps uses a `UUID` file naming scheme, with\na `lookup.json` file to map individual parameter sets back to their respective\nfiles.\n',
    'author': 'Mira Geoscience',
    'author_email': 'benjamink@mirageoscience.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mirageoscience.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
