# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strongly_typed']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'strongly-typed',
    'version': '1.0.1.post3',
    'description': 'Python module to enforce strong typing',
    'long_description': '# strongly_typed\n\nThis is a python decorator that allows you to type-check functions. Itll check the type signature of the function and, if the signature and the parameters given mismatch, will raise an exception.\n\n## Inspiration\nI wanted to use this to make sure that software i was going to write was resilient for data integrity reasons. I\'ve also learned a lot about decorators, etc.\n\n## Usage\n\n```python\nfrom strongly_typed import strongly_typed\n@strongly_typed\ndef add(a: int, b: int, message_template: str):\n    result = a + b\n    message = message_template % result\n    return message\n\nadd(1, 2, "The answer is %s!")\nadd(1, "e", 5) # raises an exception!\n```\n\n## Known issues\n- `*args` and `**kwargs` are not tested at all. This is because I\'m not sure how I\'d implement that. (Plus, I don\'t think it\'s very common to annotate those.)\n\n- Using "interchangeable" types (e.g. using an int when a float is required, or vice versa) will raise an exception. **This is by design.** The whole idea is to prevent python\'s weak typing from screwing things up. Type coercion isn\'t the only way it can do that, but it\'s one of them - and not always caught by linters.\n\n- Subclasses are not checked. So:\n\n```python\nclass Hello:\n    def hi(self):\n        print("hi")\n\nclass Subclass(Hello):\n    def __init__(self):\n        print("Init!")\n\n@strongly_typed.strongly_typed\ndef run_hi(cls: Hello):\n    cls.hi()\n\nrun_hi(Hello()) # OK\nrun_hi(Subclass()) # Raises TypeError\n```\n\nThere may be an optional feature to check if it\'s a subclass, rather than the absolute type. That\'s not a thing yet, though.\n\n## Contributing\nThe code is probably terrible. Please help me fix it! If you have any suggestions, please let me know.\n\n## Licence\n\n> Copyright 2023 TheTechRobo\n> Licensed under the Apache License, Version 2.0 (the "License");\n> you may not use this file except in compliance with the License.\n> You may obtain a copy of the License at\n>    http://www.apache.org/licenses/LICENSE-2.0\n> Unless required by applicable law or agreed to in writing, software\n> distributed under the License is distributed on an "AS IS" BASIS,\n> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n> See the License for the specific language governing permissions and\n> limitations under the License.\n\n',
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
