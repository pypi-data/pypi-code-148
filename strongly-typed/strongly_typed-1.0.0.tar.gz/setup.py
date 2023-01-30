# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strongly_typed']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'strongly-typed',
    'version': '1.0.0',
    'description': 'Python module to enforce strong typing',
    'long_description': '# strongly_typed\n\nThis is a python decorator that allows you to type-check functions. Itll check the type signature of the function and, if the signature and the parameters given mismatch, will raise an exception.\n\nTime taken: About 2 hours\n\nUsage:\n\n```python\nfrom strongly_typed import strongly_typed\n@strongly_typed\ndef add(a: int, b: int, message_template: str):\n    result = a + b\n    message = message_template % result\n    return message\n\nadd(1, 2, "The answer is %s!")\nadd(1, "e", 5) # raises an exception!\n```\n\nLicence\n\n> Copyright 2023 TheTechRobo\n> Licensed under the Apache License, Version 2.0 (the "License");\n> you may not use this file except in compliance with the License.\n> You may obtain a copy of the License at\n>    http://www.apache.org/licenses/LICENSE-2.0\n> Unless required by applicable law or agreed to in writing, software\n> distributed under the License is distributed on an "AS IS" BASIS,\n> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n> See the License for the specific language governing permissions and\n> limitations under the License.\n\n',
    'author': 'TheTechRobo',
    'author_email': 'thetechrobo@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
