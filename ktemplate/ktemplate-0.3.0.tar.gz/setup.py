# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ktemplate']

package_data = \
{'': ['*'], 'ktemplate': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

setup_kwargs = {
    'name': 'ktemplate',
    'version': '0.3.0',
    'description': 'a minimalist python html template lib',
    'long_description': '# kTemplate\n\n[![ci-badge]][ci-url] [![coverage-badge]][coverage-url] [![pypi-badge]][pypi-url] [![py-version]][py-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]\n\n> a minimalist python html template\n\n## Quick Start\n\n### Installation\n\n`pip install kTemplate`\n\n### Examples\n\n```python\nfrom kTemplate import (\n  div, img, # common html elements\n  element   # for creating custom element\n)\n\n# create common html element\n# `class` represents by `cls` due to python keyword\nhtml_str = div(img(src=\'url\'), cls=\'bar\')\n# -> <div class="bar"><img src="url"/></div>\n\n# create custom element\nmy_element = element(tag="MyElement", content="foo" props="bar")\n# -> <MyElement props="ar">foo</MyElement>\n```\n\nPlease refer to the docs for creating HTML [templates and components][components]\n\n## Documentation\n\nPlease refer the [docs] for more about:\n\n- [why] creating this package\n- [usage] details\n- function [references]\n- [contributing] guideline\n- [testing]\n- [changelog]\n\n## Need Help?\n\nOpen a [github issue](https://github.com/hoishing/kTemplate/issues) or ping me on [Twitter](https://twitter.com/hoishing) ![](https://api.iconify.design/logos/twitter.svg?width=20)\n\n[ci-badge]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml/badge.svg\n[ci-url]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml\n[coverage-badge]: https://hoishing.github.io/kTemplate/assets/coverage-badge.svg\n[coverage-url]: https://hoishing.github.io/kTemplate/assets/coverage/\n[MIT-badge]: https://img.shields.io/github/license/hoishing/kTemplate\n[MIT-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://img.shields.io/pypi/v/ktemplate\n[pypi-url]: https://pypi.org/project/ktemplate/\n[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black-url]: https://github.com/psf/black\n[py-version]: https://img.shields.io/pypi/pyversions/kTemplate\n[py-url]: https://python.org\n[docs]: https://hoishing.github.io/kTemplate/\n[why]: https://hoishing.github.io/kTemplate/why\n[usage]: https://hoishing.github.io/kTemplate/usage\n[components]: https://hoishing.github.io/kTemplate/usage/#templates-and-components\n[references]: https://hoishing.github.io/kTemplate/ref\n[contributing]: https://hoishing.github.io/kTemplate/contribute/\n[testing]: https://hoishing.github.io/kTemplate/contribute/#testing\n[changelog]: https://hoishing.github.io/kTemplate/changelog\n',
    'author': 'Kelvin Ng',
    'author_email': 'hoishing@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://hoishing.github.io/kTemplate',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
