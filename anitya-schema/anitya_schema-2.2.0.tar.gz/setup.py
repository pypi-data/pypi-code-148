# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anitya_schema', 'anitya_schema.tests']

package_data = \
{'': ['*'], 'anitya_schema.tests': ['fixtures/*']}

install_requires = \
['fedora-messaging>=3.1.0,<4.0.0']

entry_points = \
{'fedora.messages': ['anitya.distro.add = anitya_schema:DistroCreated',
                     'anitya.distro.edit = anitya_schema:DistroEdited',
                     'anitya.distro.remove = anitya_schema:DistroDeleted',
                     'anitya.project.add = anitya_schema:ProjectCreated',
                     'anitya.project.edit = anitya_schema:ProjectEdited',
                     'anitya.project.flag = anitya_schema:ProjectFlag',
                     'anitya.project.flag.set = anitya_schema:ProjectFlagSet',
                     'anitya.project.map.new = anitya_schema:ProjectMapCreated',
                     'anitya.project.map.remove = '
                     'anitya_schema:ProjectMapDeleted',
                     'anitya.project.map.update = '
                     'anitya_schema:ProjectMapEdited',
                     'anitya.project.remove = anitya_schema:ProjectDeleted',
                     'anitya.project.version.remove = '
                     'anitya_schema:ProjectVersionDeleted',
                     'anitya.project.version.remove.v2 = '
                     'anitya_schema:ProjectVersionDeletedV2',
                     'anitya.project.version.update = '
                     'anitya_schema:ProjectVersionUpdated',
                     'anitya.project.version.update.v2 = '
                     'anitya_schema:ProjectVersionUpdatedV2']}

setup_kwargs = {
    'name': 'anitya-schema',
    'version': '2.2.0',
    'description': 'JSON schema definitions for messages published by Anitya',
    'long_description': '.. image:: https://img.shields.io/pypi/v/anitya_schema.svg\n  :target: https://pypi.org/project/anitya_schema/\n\n.. image:: https://readthedocs.org/projects/anitya-messages/badge/?version=latest\n  :alt: Documentation Status\n  :target: https://anitya-messages.readthedocs.io/en/latest/?badge=latest\n\nAnitya Message Schema\n=====================\n\nJSON schema definitions for messages published by\n`Anitya <https://github.com/fedora-infra/anitya>`_.\n\nDocumentation for Anitya Message Schema could be found\n`here <https://anitya-messages.readthedocs.io/en/latest>`_.\n\nSee http://json-schema.org/ for documentation on the schema format. See\nhttps://fedora-messaging.readthedocs.io/en/latest/messages.html for\ndocumentation on fedora-messaging.\n',
    'author': 'Fedora Infrastructure Team',
    'author_email': 'infrastructure@lists.fedoraproject.org',
    'maintainer': 'Fedora Infrastructure Team',
    'maintainer_email': 'infrastructure@lists.fedoraproject.org',
    'url': 'https://github.com/fedora-infra/anitya-messages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
