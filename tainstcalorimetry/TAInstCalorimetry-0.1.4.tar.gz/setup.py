# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tainstcalorimetry']

package_data = \
{'': ['*'], 'tainstcalorimetry': ['DATA/*']}

install_requires = \
['matplotlib>=3.6.3,<4.0.0',
 'mypy>=0.991,<0.992',
 'pandas>=1.5.3,<2.0.0',
 'pysnooper>=1.1.1,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.0,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'scipy>=1.10.0,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'tainstcalorimetry',
    'version': '0.1.4',
    'description': 'Handling TAM Air calorimetry files made easy.',
    'long_description': '# TAInstCalorimetry - Interfacing with experimental results file from TAM Air calorimeters made easy.\n\nAfter collecting multiple experimental results files from a TAM Air calorimeter you will be left with multiple *.xls*-files obtained as exports from the device control software. To achieve a side by side comparison of theses results and some basic extraction of relevant parameters, **TAInstCalorimetry** is here to get this done smoothly.\n\n*Note: **TAInstCalorimetry** has been developed without involvement of **TA Instruments** and is thus independent from the company and its software.*\n\n## Info / Downloads\n\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/tainstcalorimetry.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pepy.tech/project/tainstcalorimetry)\n[![PyPI - Downloads](https://static.pepy.tech/personalized-badge/tainstcalorimetry?period=total&units=none&left_color=black&right_color=grey&left_text=Downloads)](https://pepy.tech/project/tainstcalorimetry)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tainstcalorimetry.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/tainstcalorimetry/) \n\n## Table of Contents  \n- [Example Usage](#example-usage)<br>\n  - [Basic plotting](#basic-plotting)<br>\n  - [Getting cumulated heat values](#getting-cumulated-heat-values)<br>\n  - [Identifying peaks](#identifying-peaks)<br>\n  - [Identifying peak onsets](#identifying-peak-onsets)<br>\n- [Installation](#installation)<br>\n- [Contributing](#contributing)\n\n## Example Usage\n\nImport the ```tacalorimetry``` module from **TAInstCalorimetry**.\n\n```python\n# import\nimport os\nfrom TAInstCalorimetry import tacalorimetry\n```\n\nNext, we define where the exported files are stored. With this information at hand, a ```Measurement``` is initialized. Experimental raw data and the metadata passed in the course of the measurement are retrieved by the methods ```get_data()``` and ```get_information()```, respectively.\n\n```python\n# define data path\n# "mycalodata" is the subfoldername where the calorimetry\n# data files (both .csv or .xlsx) are stored\n\npathname = os.path.dirname(os.path.realpath(__file__))\npath_to_data = pathname + os.sep + "mycalodata"\n\n# Example: if projectfile is at "C:\\Users\\myname\\myproject\\myproject.py", then "mydata"\n# refers to "C:\\Users\\myname\\myproject\\mycalodata" where the data is stored\n\n# load experiments via class, i.e. instantiate tacalorimetry object with data\ntam = tacalorimetry.Measurement(folder=path_to_data)\n\n# get sample and information\ndata = tam.get_data()\ninfo = tam.get_information()\n```\n\n### Basic plotting\n\nFurthermore, the ```Measurement``` features a ```plot()```-method for readily visualizing the collected results.\n\n```python\n# make plot\ntam.plot()\n# show plot\ntacalorimetry.plt.show()\n```\n\nWithout further options specified, the ```plot()```-method yields the following.\n\n![enter image description here](https://github.com/mj-hofmann/TAInstCalorimetry/blob/main/tests/plots/Figure%202022-08-08%20112743.png?raw=true)\n\nThe ```plot()```-method can also be tuned to show the temporal course of normalized heat.\n\n```python\n# show cumulated heat plot\nax = tam.plot(\n    t_unit="h",\n    y=\'normalized_heat\',\n    y_unit_milli=False\n)\n\n# define target time\ntarget_h = 1.5\n\n# guide to the eye line\nax.axvline(target_h, color="gray", alpha=0.5, linestyle=":")\n\n# set upper limits\nax.set_ylim(top=250)\nax.set_xlim(right=6)\n# show plot\ntacalorimetry.plt.show())\n```\nThe following plot is obtained:\n\n![enter image description here](https://github.com/mj-hofmann/TAInstCalorimetry/blob/main/tests/plots/Figure%202022-08-19%20085928.png?raw=true)\n\n### Getting cumulated heat values\n\nThe cumulated heat after a certain period of time ```target_h``` from starting the measurement is a relevant quantity for answering different types of questions. For this purpose, the method ```get_cumulated_heat_at_hours``` returns an overview of this parameter for all the samples in the specified folder.\n\n```python\n# get table of cumulated heat at certain age\ncumulated_heats = tam.get_cumulated_heat_at_hours(\n          target_h=target_h,\n          cutoff_min=10\n          )\n          \n# show result\nprint(cumulated_heats)\n```\n\nThe return value of the method, ```cumulated_heats``` is a ```pd.DataFrame```.\n\n### Identifying peaks\n\nNext to cumulated heat values detected after a certain time frame from starting the reaction, peaks characteristics can be obtained from the experimental data via the ```get_peaks```-method.\n\n```python\n# get peaks\npeaks = tam.get_peaks(\n    show_plot=True,\n    prominence=0.00001,  # "sensitivity of peak picking"\n    cutoff_min=60,  # how much to discard at the beginning of the measurement\n    plt_right_s=4e5,\n    plt_top=1e-2,\n    regex=".*_\\d"  # filter samples\n    )\n```\n\nTweaking some of the available keyword arguments, the following plot is obtained:\n\n![Identified peaks for one sample.](https://github.com/mj-hofmann/TAInstCalorimetry/blob/main/tests/plots/Figure%202023-01-25%20193222.png?raw=true)\n\n### Identifying peak onsets\n\nSimilarly, the peak onset characteristics are accessible via the ```get_peak_onsets```-method. The resulting plot is shown below.\n\n```python\n# get onsets\nonsets = tam.get_peak_onsets(\n    gradient_threshold=0.000001,\n    rolling=10,\n    exclude_discarded_time=True,\n    show_plot=True,\n    regex="OPC"\n)\n```\n![Identified peak onsets for one sample.](https://github.com/mj-hofmann/TAInstCalorimetry/blob/main/tests/plots/Figure%202023-01-26%20174524.png?raw=true)\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install TAInstCalorimetry.\n\n```bash\npip install TAInstCalorimetry\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\nList of contributors:\n- tgaedt\n- mj-hofmann\n\n## License\n[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/#)\n\n\n## Test\n![Tests](https://github.com/mj-hofmann/TAInstCalorimetry/actions/workflows/run-tests.yml/badge.svg)\n\n## Code Styling\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n',
    'author': 'mj-hofmann',
    'author_email': 'aCodingChemist@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mj-hofmann/TAInstCalorimetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8.1,<3.12',
}


setup(**setup_kwargs)
