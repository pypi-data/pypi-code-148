# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangocms_themata',
 'djangocms_themata.management.commands',
 'djangocms_themata.migrations',
 'djangocms_themata.templatetags']

package_data = \
{'': ['*'], 'djangocms_themata': ['templates/*', 'templates/themata/*']}

install_requires = \
['Django>=3.2,<4.0',
 'django-cms>=3.9.0,<4.0.0',
 'djangocms-bootstrap>=1.1.2,<2.0.0',
 'djangocms-page-meta>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'djangocms-themata',
    'version': '0.1.1',
    'description': 'A set of themes for Django CMS projects.',
    'long_description': '==================\ndjangocms-themata\n==================\n\nA set of themes for Django CMS projects.\n\nInstallation\n============\n\nInstall with pip from PyPI:\n\n.. code-block:: bash\n\n    pip install djangocms-themata\n\nOr install directory from Github:\n\n.. code-block:: bash\n\n    pip install git+https://github.com/rbturnbull/djangocms-themata\n\n\nUsage\n========\n\nStart with a Django project set up with `Django CMS <https://docs.django-cms.org/en/latest/how_to/install.html>`_.\n\nAdd ``djangocms_themata`` to the list of plugins:\n\n.. code-block:: python\n\n    INSTALLED_APPS += [\n        "djangocms_themata",\n    ]\n\nGet your templates to extend ``base.html``:\n\n.. code-block:: jinja2\n\n    {% extends "base.html" %}\n\nTo import stylesheets from bootswatch (https://bootswatch.com/) run this command:\n\n.. code-block:: bash\n\n    ./manage.py importbootswatch\n\nThen navigate to the admin section of the website and go to the djangocms-themata section. Activate the theme that you like there.\n\nCredits\n========\n\nApp designed by Robert Turnbull (Melbourne Data Analytics Platform)\n\nAll bootstrap themes are taken from the bootswatch CDN.\n\n',
    'author': 'Robert Turnbull',
    'author_email': 'robert.turnbull@unimelb.edu.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rbturnbull/djangocms-themata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
