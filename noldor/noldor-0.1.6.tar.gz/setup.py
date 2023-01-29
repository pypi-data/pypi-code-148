# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noldor', 'noldor.validators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'noldor',
    'version': '0.1.6',
    'description': 'A validation library easy to extend.',
    'long_description': '# Noldor\n\nNoldor is a Python validation library easy to extend.\n\nIt is easily compatible with [dataclasses](https://docs.python.org/3/library/dataclasses.html), [attrs](https://github.com/python-attrs/attrs) and [pydantic](https://github.com/pydantic/pydantic).\n\n## Installation\n\n```\npip install noldor\n```\n\n## Usage with classes\n\nAssume you have the following class defined:\n\n```python\nclass Person:\n    \n    name: str\n    age: int\n```\n\nYou want to be sure that the name string is longer than zero characters and also that the age is an integer value greater than 0.\n\n### Dataclass\n\n```python\nfrom dataclasses import dataclass\nfrom noldor import validate\nfrom noldor.validators import longer_than, greater_than\n\n@dataclass\nclass Person:\n    \n    name: str\n    age: int\n\n    def __post_init__(self) -> None:\n        validate(self.name, longer_than(0))\n        validate(self.age, greater_than(0))\n```\n\n### Attrs\n```python\nfrom attrs import define\nfrom noldor import validate\nfrom noldor.validators import longer_than, greater_than\n\n@define\nclass Person:\n    \n    name: str\n    age: int\n\n    def __attrs_post_init__(self) -> None:\n        validate(self.name, longer_than(0))\n        validate(self.age, greater_than(0))\n```\n\n\n### Pydantic\n\n```python\nfrom pydantic.dataclasses import dataclass\nfrom noldor import validate\nfrom noldor.validators import longer_than, greater_than\n\n@dataclass\nclass Person:\n\n    name: str\n    age: int\n\n    def __post_init__(self) -> None:\n        validate(self.name, longer_than(0))\n        validate(self.age, greater_than(0))\n```\n\nIn any case, if you create a Person object that does not respect the given constraints, a ValueError is raised. The ValueError contains the log of the validation process as the first argument.\n\n```python\n>>> p = Person(name="Max", age=-1)\n\n...\n\nValueError: [red]NOT RESPECTED[/red]: -1 must be greater than 0\n```\n\n### Multiple constraints for one value\n\nNotice that you can specify multiple constraints on a given value. For example, if you want the name of a Person to be also shorter than 30 characters (example given only with dataclasses for simplicity):\n\n```python\nfrom dataclasses import dataclass\nfrom noldor import validate\nfrom noldor.validators import longer_than, shorter_than, greater_than\n\n@dataclass\nclass Person:\n    \n    name: str\n    age: int\n\n    def __post_init__(self) -> None:\n        validate(self.name, longer_than(0), shorter_than(30))\n        validate(self.age, greater_than(0))\n```\n\n## General usage\nNoldor is probably perfectly compatible with other libraries and its usage is not restricted to the validation of class attributes. In fact, Noldor can be exploited for validating any kind of value.\n\nFor example, imagine you got an integer value from the user input. You want to check that the value is a positive prime integer. You can do this way:\n\n```python\nfrom noldor import validate\nfrom noldor.validators import is_positive, is_prime\n\nif __name__ == "__main__":\n    N = int(input())\n    validate(N, is_positive(), is_prime())\n```\n\nIf you do not want to throw a ValueError when a constraint is not satisfied, you can use the `check` function. This function returns a `Response` object, containing a boolean value that represents the result of the validation (True if all conditions are satisfied, False if at least one condition is not satisfied):\n\n```python\nfrom noldor import check\nfrom noldor.validators import is_positive, is_prime\n\nif __name__ == "__main__":\n    N = int(input())\n    res = check(N, is_positive(), is_prime())\n    if res.result is True:\n        print(f"{N} is a valid value!", res.log)\n    else:\n        print(f"{N} is **not** a valid value.", res.log)\n```\n\n## Create your custom validator\n\nWe call "validator" a function returning a Validator object.\nA Validator object contains:\n- a *condition*: a function that returns a boolean value;\n- a *name*: a name for the validator, exploited to write the log of the validation.\n\nHere follows the definition of the validator `multiple_of`:\n\n```python\ndef longer_than(lower_bound: int) -> Validator[Sized]:\n    return Validator[Sized](\n        lambda x: len(x) > lower_bound,\n        f"longer than {lower_bound}"\n    )\n```\n\nYou can find a lot of examples of validators in the folder `noldor/validators`.\n\nNoldor is a tiny library, easy to expand. If you write a validator that can be useful to many others, feel free to issue a pull request!',
    'author': 'Nicolò Sala',
    'author_email': 'nicolo.sala@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitea.nicheosala.xyz/nicheosala/noldor',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
