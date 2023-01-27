# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docx',
 'docx.dml',
 'docx.enum',
 'docx.image',
 'docx.opc',
 'docx.opc.parts',
 'docx.oxml',
 'docx.oxml.text',
 'docx.parts',
 'docx.styles',
 'docx.text']

package_data = \
{'': ['*'],
 'docx': ['templates/*',
          'templates/default-docx-template/*',
          'templates/default-docx-template/_rels/*',
          'templates/default-docx-template/docProps/*',
          'templates/default-docx-template/word/*',
          'templates/default-docx-template/word/_rels/*',
          'templates/default-docx-template/word/theme/*']}

install_requires = \
['behave>=1.2.6,<2.0.0', 'lxml>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'python-docx-ng',
    'version': '0.9.3',
    'description': 'python-docx-ng is a Python library for creating and updating Microsoft Word (.docx) files.',
    'long_description': '# python-docx-ng\n\n*python-docx-ng* is a Python library for creating and updating Microsoft Word (.docx) files.\nIt was originally designed and developed by [scanny](https://github.com/scanny) as [python-docx](https://github.com/python-openxml/python-docx).\nAs he is not actively developing his repo and there are soo many useful pull requests, bringing together a more powerful tool.\nThis repo should merge a lot of those things and create a more powerful version, hopefully bearing the original structure of scanny in mind.\n\nA new documentation section will be build up soon based on Markdown in the [docs](docs) section.\nExamples can be found here: [examples](docs/examples)\nOlder information is available in the [python-docx Documentation](https://python-docx.readthedocs.org/en/latest/).\n\n## Installation\n\n```commandline\npip install python-docx-ng\n```\n\n> Hint: The library is called `docx` in python scripts, so use imports like `import docx`. \n\n## Features\n\n+ [x] Word 16 (Office 2019) Template ([54a1269](https://github.com/toxicphreAK/python-docx-ng/commit/54a1269a3608239adfef079840f69389235c88b8))\n+ [x] Faster & improved tables ([#1](https://github.com/toxicphreAK/python-docx-ng/pull/1))\n+ [x] SVG support ([#4](https://github.com/toxicphreAK/python-docx-ng/pull/4))\n+ [x] Font scaling ([#6](https://github.com/toxicphreAK/python-docx-ng/pull/6))\n+ [x] Outline level ([#7](https://github.com/toxicphreAK/python-docx-ng/pull/7)) - shows outline in navigation (e.g. Word or PDF application - not affecting the document itself)\n+ [x] RGB color font highlighting ([#14](https://github.com/toxicphreAK/python-docx-ng/pull/14))\n+ [x] Hyperlink text ([#16](https://github.com/toxicphreAK/python-docx-ng/pull/16))\n+ [x] `.docm` file support ([#19](https://github.com/toxicphreAK/python-docx-ng/pull/16)) - enables marco documents\n+ [x] Form fields & AltChunk support ([#20](https://github.com/toxicphreAK/python-docx-ng/pull/20))\n+ [x] Custom namespaces ([#21](https://github.com/toxicphreAK/python-docx-ng/pull/21))\n+ [x] Performance improvements\n  + Paragraph.text ([#3}(https://github.com/toxicphreAK/python-docx-ng/pull/3)\n  + Cache for table cells ([#8](https://github.com/toxicphreAK/python-docx-ng/pull/8))\n+ [x] Fixes\n  + add_picture ([#10](https://github.com/toxicphreAK/python-docx-ng/pull/10)) - fix next_id to support multiple pictures\n  + `Heading 1` key error due to style capitalization (e.g. in LibreOffice) ([#12](https://github.com/toxicphreAK/python-docx-ng/pull/12))\n  + Fix XPath for sectPr in document ([#15](https://github.com/toxicphreAK/python-docx-ng/pull/15))\n  + Reproducible documents ([#17](https://github.com/toxicphreAK/python-docx-ng/pull/17)) - same binary output with same data\n  + AttValue too long in etree xml parser ([#24](https://github.com/toxicphreAK/python-docx-ng/pull/24))\n\n## Roadmap\n\n+ [ ] Document all functionallities building a new sample document with *all* (most) features included\n+ [ ] Remove code references to original repo of python-docx\n+ [ ] Setup new docs (markdown based)\n+ [ ] Add missing tests\n',
    'author': 'toxicphreAK',
    'author_email': 'pentesting.laboratories@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
