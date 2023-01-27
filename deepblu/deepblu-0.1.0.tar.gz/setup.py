# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deepblu', 'deepblu.di']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deepblu',
    'version': '0.1.0',
    'description': 'Library for advanced architectures/patterns in modern Python. Domain-Driven Design (DDD), CQRS, Event Sourcing, Event-driven architectures, message queues, unit of work dependency injection and more.',
    'long_description': '# deepblu\nLibrary for advanced architectures/patterns in modern Python. Domain-Driven Design (DDD), CQRS, Event Sourcing, Event-driven architectures, message queues, unit of work and more.\n\n[WORK IN PROGRESS]',
    'author': 'Carlo Casorzo',
    'author_email': 'carlo@deepblu.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
