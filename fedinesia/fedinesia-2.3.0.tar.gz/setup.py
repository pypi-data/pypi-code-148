# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fedinesia']

package_data = \
{'': ['*']}

install_requires = \
['aiocsv>=1.2.3,<2.0.0',
 'aiofiles>=0.8.0,<0.9.0',
 'arrow>=1.2.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'minimal-activitypub>=0.4.0,<0.5.0',
 'outdated>=0.2.1,<0.3.0',
 'rich>=13.0.0,<14.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing-extensions>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['fedinesia = fedinesia.amnesia:start']}

setup_kwargs = {
    'name': 'fedinesia',
    'version': '2.3.0',
    'description': 'Deletes old posts from fediverse accounts. Confirmed working with Mastodon and Pleroma (and Forks)',
    'long_description': '""""""""""""""""""""""""""\nFedinesia\n""""""""""""""""""""""""""\n\n|Repo| |CI| |Downloads|\n\n|Checked against| |Checked with| |Interrogate|\n\n|Code style| |Version| |Wheel|\n\n|AGPL|\n\n\n***!!! BEWARE, THIS TOOL WILL DELETE SOME OF YOUR POSTS ON THE FEDIVERSE !!!***\n\nFedinesia is a command line (CLI) tool to delete old statuses from Mastodon or Pleroma instances.\nIt respects rate limits imposed by servers.\n\nInstall and run from `PyPi <https://pypi.org>`_\n=================================================\n\nIt\'s ease to install Fedinesia from Pypi using the following command::\n\n    pip install fednesia\n\nOnce installed Fedinesia can be started by typing ``fedinesia`` into the command line.\n\nInstall and run from `Source <https://codeberg.org/MarvinsMastodonTools/fedinesia>`_\n==============================================================================================\n\nAlternatively you can run Fedinesia from source by cloning the repository using the following command line::\n\n    git clone https://codeberg.org/MarvinsMastodonTools/fedinesia.git\n\nFedinesia uses `Poetry <https://python-poetry.org/>`_ for dependency control, please install Poetry before proceeding further.\n\nBefore running, make sure you have all required python modules installed. With Poetry this is as easy as::\n\n    poetry install --only main\n\nRun Fedinesia with the command `poetry run fedinesia`\n\nConfiguration / First Run\n=========================\n\nFedinesia will ask for all necessary parameters when run for the first time and store them in ```config.json``\nfile in the current directory.\n\nLicensing\n=========\nFedinesia is licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_\n\nSupporting Fedinesia\n==========================\n\nThere are a number of ways you can support Fedinesia:\n\n- Create an issue with problems or ideas you have with/for Fedinesia\n- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.\n- You can send me small change in Monero to the address below:\n\nMonero donation address\n-----------------------\n``86ZnRsiFqiDaP2aE3MPHCEhFGTeipdQGJZ1FNnjCb7s9Gax6ZNgKTyUPmb21WmT1tk8FgM7cQSD5K7kRtSAt1y7G3Vp98nT``\n\n\n.. |AGPL| image:: https://www.gnu.org/graphics/agplv3-with-text-162x68.png\n    :alt: AGLP 3 or later\n    :target:  https://codeberg.org/MarvinsMastodonTools/fedinesia/src/branch/main/LICENSE.md\n\n.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue\n    :alt: Repo at Codeberg.org\n    :target: https://codeberg.org/MarvinsMastodonTools/fedinesia\n\n.. |Downloads| image:: https://pepy.tech/badge/fedinesia\n    :alt: Download count\n    :target: https://pepy.tech/project/fedinesia\n\n.. |Code style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :alt: Code Style: Black\n    :target: https://github.com/psf/black\n\n.. |Checked against| image:: https://img.shields.io/badge/Safety--DB-Checked-green\n    :alt: Checked against Safety DB\n    :target: https://pyup.io/safety/\n\n.. |Checked with| image:: https://img.shields.io/badge/pip--audit-Checked-green\n    :alt: Checked with pip-audit\n    :target: https://pypi.org/project/pip-audit/\n\n.. |Version| image:: https://img.shields.io/pypi/pyversions/fedinesia\n    :alt: PyPI - Python Version\n\n.. |Wheel| image:: https://img.shields.io/pypi/wheel/fedinesia\n    :alt: PyPI - Wheel\n\n.. |CI| image:: https://ci.codeberg.org/api/badges/MarvinsMastodonTools/fedinesia/status.svg\n    :alt: CI / Woodpecker\n    :target: https://ci.codeberg.org/MarvinsMastodonTools/fedinesia\n\n.. |Interrogate| image:: https://codeberg.org/MarvinsMastodonTools/fedinesia/raw/branch/main/interrogate_badge.svg\n    :alt: Doc-string coverage\n    :target: https://interrogate.readthedocs.io/en/latest/\n',
    'author': 'marvin8',
    'author_email': 'marvin8@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/MarvinsMastodonTools/fedinesia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
