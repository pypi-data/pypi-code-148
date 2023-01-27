# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssb_sparktools',
 'ssb_sparktools.editing',
 'ssb_sparktools.logging',
 'ssb_sparktools.processing',
 'ssb_sparktools.quality',
 'ssb_sparktools.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.5,<1.24.0', 'pandas>=1.5.1,<2.0.0', 'pyspark>=3.3.1,<3.4.0']

setup_kwargs = {
    'name': 'ssb-spark-tools',
    'version': '0.1.10',
    'description': 'A collection of data processing Spark functions for the use in Statistics Norway.',
    'long_description': '# SSB Spark Tools\n\n> A collection of data processing Spark functions for the use in Statistics Norway (SSB)\n\n[![PyPI version](https://img.shields.io/pypi/v/ssb_spark_tools.svg)](https://pypi.python.org/pypi/ssb_spark_tools/)\n[![Status](https://img.shields.io/pypi/status/ssb_spark_tools.svg)](https://pypi.python.org/pypi/ssb_spark_tools/)\n[![License](https://img.shields.io/pypi/l/ssb_spark_tools.svg)](https://pypi.python.org/pypi/ssb_spark_tools/)\n\nThe SSB Spark Tools Library is a colection of Data processing functions for the use in Data processing in Statistics Norway\n\n## Installation\n\n```python\npip install ssb-spark-tools\n```\n\n## Development setup\n\nThis repo uses `poetry` for dependency management and publishing to PyPi.\nInstall poetry as described on the [poetry install page](https://python-poetry.org/docs/#installation).\n\n```\npoetry install                 Install required tools for build/dev\npoetry run pytest              Run tests\npoetry build                   Build dist\npoetry publish                 Publish to PyPi\n```\n\n### Testing\n\nRun tests for all python distributions using GitHub Actions,\nsee https://github.com/statisticsnorway/SSB_Spark_tools/actions\n\n## Releasing\n\n_Prerequisites:_\nYou will need to register accounts on [PyPI](https://pypi.org/account/register/) and [TestPyPI](https://test.pypi.org/account/register/).\n\nBefore releasing:\n\n- Make sure you\'re working on a "new" version number.\n- Make sure to update release notes.\n- Make sure the GitHub repo has a secret with the name `PYPI_API_TOKEN`\n  and contains the PyPi access token.\n\nTo release and publish a new version to PyPI:\n\n- Create a new release in the GitHub repo.\n- The `Upload Python Package` GitHub Action will start and publish the new version to PyPi.\n\nManually:\n\n```sh\npoetry publish\n```\n\nFor a dress rehearsal, you can do a test release to the [TestPyPI index](https://test.pypi.org/). TestPyPI is very useful, as you can try all the steps of publishing a package without any consequences if you mess up. Read more about TestPyPI [here](https://packaging.python.org/guides/using-testpypi/).\n\nYou should see the new release appearing [here](https://pypi.org/project/ssb-spark-tools/) (it might take a couple of minutes for the index to update).\n\n## Release History\n\n- 0.0.1\n  - Initial version with functions as in use on initiaition\n\n## Meta\n\nStatistics Norway – https://github.com/statisticsnorway\n\nDistributed under the MIT license. See `LICENSE` for more information.\n\n<https://github.com/statisticsnorway/SSB_Spark_tools>\n\n## Contributing\n\n1. Fork it (<https://github.com/statisticsnorway/SSB_Spark_tools/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am \'Add some fooBar\'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n',
    'author': 'Statistics Norway',
    'author_email': '81353974+arneso-ssb@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
