# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hoppr',
 'hoppr.base_plugins',
 'hoppr.cli',
 'hoppr.configs',
 'hoppr.core_plugins',
 'hoppr.hoppr_types',
 'hoppr.models']

package_data = \
{'': ['*'], 'hoppr': ['resources/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'hoppr-cyclonedx-models==0.3.0',
 'in-toto>=1.2.0,<2.0.0',
 'jc>=1.22.2,<2.0.0',
 'jmespath>=1.0.1,<2.0.0',
 'oras>=0.1.0,<0.2.0',
 'packageurl-python>=0.10.0,<0.11.0',
 'pydantic-yaml>=0.8.1,<0.9.0',
 'pydantic[email]>=1.9.0,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'types-PyYAML>=6.0.5,<7.0.0']

entry_points = \
{'console_scripts': ['hopctl = hoppr.cli.hopctl:app']}

setup_kwargs = {
    'name': 'hoppr',
    'version': '1.7.0',
    'description': 'A tool for defining, verifying, and transferring software dependencies between environments.',
    'long_description': "![Hoppr repository banner](media/hoppr-repo-banner.png)\n\n---\n## What is Hoppr?\n\nHoppr is a Python plugin-based framework for collecting, processing, and bundling your software supply chain.\nFeed Hoppr your [CycloneDX spec SBOMs](https://cyclonedx.org/specification/overview/) (Software Bill of Materials) and receive enhanced\nSBOMs and component bundles in return!  Those are just the basics, learn more at:\n\n**The Documentation**: <https://hoppr.dev>\n\n**Source Code**: <https://gitlab.com/hoppr/hoppr>\n\n---\n\n## Getting Started\n\nFor a full Hoppr startup, we recommend the [`Your First Bundle` tutorial](https://hoppr.dev/docs/get-started/your-first-bundle)\n\nInstall [Hoppr from PyPI](https://pypi.org/project/hoppr/)\n```\npip install hoppr\n```\n\n## Join Us!\n\nWe're completely open source, [MIT licensed](LICENSE), and community friendly. Built with a plugin architecture, Hoppr enables users to extend its SBOM-processing capabilities through their own plugins and algorithms.  \n[Learn more](https://hoppr.dev/docs/development/contributing) on how to contribute, it's easy and welcoming!",
    'author': 'LMCO Open Source',
    'author_email': 'open.source@lmco.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hoppr.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
