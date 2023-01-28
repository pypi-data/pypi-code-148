# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['koda_validate', 'koda_validate.serialization']

package_data = \
{'': ['*']}

install_requires = \
['koda==1.4.0']

setup_kwargs = {
    'name': 'koda-validate',
    'version': '3.1.1',
    'description': 'Typesafe, composable validation',
    'long_description': "# Koda Validate\n\nBuild typesafe validators automatically or explicitly -- or write your own. Combine them to\nbuild validators of arbitrary complexity. Koda Validate is async-friendly, pure Python, and\n1.5x - 12x faster than Pydantic.\n\nDocs: [https://koda-validate.readthedocs.io/en/stable/](https://koda-validate.readthedocs.io/en/stable/)\n\n```python\n\nfrom typing import TypedDict \nfrom koda_validate import (StringValidator, MaxLength, MinLength, \n                           ListValidator, TypedDictValidator)\nfrom koda_validate.signature import validate_signature\n\n# Explicit Validators\nstring_validator = StringValidator(MinLength(8), MaxLength(20))\n\nlist_string_validator = ListValidator(string_validator)\n\n\n# Derived Validators\nclass Person(TypedDict):\n    name: str\n    hobbies: list[str] \n\nperson_validator = TypedDictValidator(Person)\n\n\n# Runtime type checking\n@validate_signature\ndef add(a: int, b: int) -> int:\n    return a + b\n\n```\n\nThere's much, much more... Check out the [Docs](https://koda-validate.readthedocs.io/en/stable/).\n\n\n## Something's Missing Or Wrong \nOpen an [issue on GitHub](https://github.com/keithasaurus/koda-validate/issues) please!\n",
    'author': 'Keith Philpott',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/keithasaurus/koda-validate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
