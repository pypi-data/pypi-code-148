# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ffpack',
 'ffpack.fdm',
 'ffpack.lcc',
 'ffpack.lsg',
 'ffpack.lsm',
 'ffpack.rpm',
 'ffpack.rrm',
 'ffpack.utils']

package_data = \
{'': ['*']}

extras_require = \
{':python_version == "3.7"': ['scipy>=1.2,<1.8'],
 ':python_version >= "3.8" and python_version < "3.11"': ['scipy>=1.8,<2.0']}

setup_kwargs = {
    'name': 'ffpack',
    'version': '0.3.1',
    'description': 'Fatigue and fracture package',
    'long_description': '# FFPACK - Fatigue and Fracture PACKage\n\n![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dpzhuX/ffpack/python-package.yml?color=brightgreen&label=Test&logo=github&logoColor=white)\n![PyPI](https://img.shields.io/pypi/v/ffpack?color=brightgreen&label=PyPI&logo=python&logoColor=white)\n![GitHub](https://img.shields.io/github/license/dpzhuX/ffpack?color=brightgreen&logo=gnu&label=License&logoColor=white)\n![Read the Docs](https://img.shields.io/readthedocs/ffpack?color=brigthgreen&label=Docs&logo=read%20the%20docs&logoColor=white)\n[![Downloads](https://static.pepy.tech/personalized-badge/ffpack?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/ffpack)\n[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.7478424-blue.svg?logo=Buffer&logoColor=white)](https://doi.org/10.5281/zenodo.7478424)\n\n\n## Purpose\n`FFPACK` ( Fatigue and Fracture PACKage ) is an open-source Python library for fatigue and fracture analysis. It supports ASTM cycle counting, load sequence generation, fatigue damage evaluation, etc. A lot of features are under active development. `FFPACK` is designed to help engineers analyze fatigue and fracture behavior in engineering practice.\n\n## Installation\n\n`FFPACK` can be installed via [PyPI](https://pypi.org/project/ffpack/):\n\n```bash\npip install ffpack\n```\n\n## Usage\n\nThe following example shows the usage of ASTM rainflow counting,\n\n```python\n# Import the ASTM rainflow counting function\nfrom ffpack.lcc import astmRainflowCounting\n\n# Prepare the data\ndata = [ -2.0, 1.0, -3.0, 5.0, -1.0, 3.0, -4.0, 4.0, -2.0 ]\n\n# Get counting results\nresults = astmRainflowCounting( data )\n```\n\nSee the package document for more details and examples.\n\n## Status\n\n`FFPACK` is currently under active development. \n\n## Contents\n\n* Fatigue damage model\n    * Palmgren-miner damage model\n        * Naive Palmgren-miner damage model\n        * Classic Palmgren-miner damage model\n\n* Load correction and counting\n    * ASTM counting\n        * ASTM level crossing counting\n        * ASTM peak counting\n        * ASTM simple range counting\n        * ASTM range pair counting\n        * ASTM rainflow counting\n        * ASTM rainflow counting for repeating history\n    * Johannesson counting\n        * Johannesson min max counting\n    * Rychlik counting\n        * Rychlik rainflow counting\n    * Four point counting\n        * Four point rainflow counting\n\n* Load sequence generator\n    * Random walk\n        * Uniform random walk\n    * Autoregressive moving average model\n        * Normal autoregressive (AR) model\n        * Normal moving average (MA) model\n        * Normal ARMA model\n        * Normal ARIMA model\n    * Sequence from spectrum\n        * Spectral representation\n\n* Load spectra and matrices\n    * Cycle counting matrix\n        * ASTM simple range counting matrix\n        * ASTM range pair counting matrix\n        * ASTM rainflow counting matrix\n        * ASTM rainflow counting matrix for repeating history\n        * Johannesson min max counting matrix\n        * Rychlik rainflow counting matrix\n        * Four point rainflow counting matrix\n    * Wave spectra\n        * Jonswap spectrum\n        * Pierson Moskowitz spectrum\n        * ISSC spectrum\n        * Gaussian Swell spectrum\n        * Ochi-Hubble spectrum\n    * Wind spectra\n        * Davenport spectrum with drag coefficient\n        * Davenport spectrum with roughness length\n        * EC1 spectrum\n        * IEC spectrum\n        * API spectrum\n    * Sequence spectra\n        * Periodogram spectrum\n        * Welch spectrum\n\n* Random and probabilistic model\n    * Metropolis-Hastings algorithm\n        * Metropolis-Hastings sampler\n        * Au modified Metropolis-Hastings sampler\n    * Nataf algorithm\n        * Nataf transformation\n\n* Risk and reliability model\n    * First order second moment\n        * Mean value FOSM\n    * First order reliability method\n        * Hasofer-Lind-Rackwitz-Fiessler FORM\n        * Constrained optimization FORM\n    * Second order reliability method\n        * Breitung SORM\n        * Tvedt SORM\n        * Hohenbichler and Rackwitz SORM\n    * Simulation based reliability method\n        * Subset simulation\n\n* Utility \n    * Aggregation\n        * Cycle counting aggregation\n    * Counting matrix\n        * Counting results to counting matrix\n    * Fitter\n        * SN curve fitter\n    * Sequence filter\n        * Sequence peakValley filter\n        * Sequence hysteresis filter\n    * Degitization\n        * Sequence degitization\n    * Derivatives\n        * Derivative\n        * Central derivative weights\n        * Gradient\n        * Hessian matrix\n\n## Document\n\nYou can find the latest documentation for setting up `FFPACK` at the [Read the Docs site](https://ffpack.readthedocs.io/en/latest/).\n\n## Credits\n\nThis project was made possible by the help from [DM2L lab](https://dm2l.uconn.edu/).\n\n## License\n\n[GPLv3](https://github.com/dpzhuX/ffpack/blob/main/LICENSE)\n',
    'author': 'Dongping Zhu',
    'author_email': 'None',
    'maintainer': 'Dongping Zhu',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/ffpack',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
