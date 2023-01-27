# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyopenair']

package_data = \
{'': ['*'], 'pyopenair': ['templates/*']}

install_requires = \
['Shapely>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyopenair = pyopenair.main:cli']}

setup_kwargs = {
    'name': 'pyopenair',
    'version': '1.2.0',
    'description': 'A simple python package to convert geo data to OpenAir format',
    'long_description': 'pyOpenair, a WKT 2 OpenAir converter\n************************************\n\nA simple package to convert geo data from `WKT <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_ to `OpenAir format <http://www.winpilot.com/usersguide/userairspace.asp>`_.\n\nThis project has been developped by LPO Auvergne-Rhône-Alpes to add `OpenAir <http://www.winpilot.com/UsersGuide/UserAirspace.asp>`_ export feature in `GeoTrek-admin <https://github.com/GeotrekCE/Geotrek-admin>`_ to sensitivity module for aerial areas.\n\n\nDocumentation\n#############\n\n`<https://pyopenair.readthedocs.io/en/latest/>`_\n\nInstallation\n############\n\n.. code:: console\n\n    pip install pyopenair\n\n\nLicence\n#######\n\n`GNU GPLv3 <https://www.gnu.org/licenses/gpl.html>`_\n\nTeam\n####\n\n* `@lpofredc <https://github.com/lpofredc/>`_ (`LPO Auvergne-Rhône-Alpes <https://github.com/lpoaura/>`_), main developper\n* `@BPascal-91 <https://github.com/BPascal-91>`_ for advices, tests and recommendations\n\n\n.. image:: https://raw.githubusercontent.com/lpoaura/biodivsport-widget/master/images/LPO_AuRA_l250px.png\n    :align: center\n    :height: 100px\n    :alt: alternate text',
    'author': 'lpofredc',
    'author_email': 'frederic.cloitre@lpo.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lpoaura/pyopenair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.2,<4.0.0',
}


setup(**setup_kwargs)
