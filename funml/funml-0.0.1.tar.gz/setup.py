# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['funml', 'funml.data']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'funml',
    'version': '0.0.1',
    'description': 'A collection of utilities to help write python as though it were an ML-kind of functional language like OCaml',
    'long_description': '# FunML\n\n[![PyPI version](https://badge.fury.io/py/funml.svg)](https://badge.fury.io/py/funml) ![CI](https://github.com/sopherapps/funml/actions/workflows/CI.yml/badge.svg)\n\nA collection of utilities to help write python as though it were an ML-kind of functional language like OCaml\n\n**The API is still unstable. Use at your own risk.**\n\n---\n\n**Documentation:** [https://sopherapps.github.io/funml](https://sopherapps.github.io/funml)\n\n**Source Code:** [https://github.com/sopherapps/funml](https://github.com/sopherapps/funml)\n\n--- \n\nMost Notable Features are:\n\n1. Immutable data structures like enums, records, lists\n2. Piping outputs of one function to another as inputs. That\'s how bigger functions are created from smaller ones.\n3. Pattern matching for declarative conditional control of flow instead of using \'if\'s\n4. Error handling using the `Result` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch09-02-recoverable-errors-with-result.html).\n   Instead of using `try-except` all over the place, functions return \n   a `Result` which has the right data when successful and an exception if unsuccessful. \n   The result is then pattern-matched to retrieve the data or react to the exception.\n5. No `None`. Instead, we use the `Option` monad, courtesy of [rust](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html?highlight=option#the-option-enum-and-its-advantages-over-null-values).\n   When an Option has data, it is `Option.SOME`, or else it is `Option.NONE`. \n   Pattern matching helps handle both scenarios.\n\n## Dependencies\n\n- [python 3.7+](https://docs.python.org/)\n\n## Contributing\n\nContributions are welcome. The docs have to maintained, the code has to be made cleaner, more idiomatic and faster,\nand there might be need for someone else to take over this repo in case I move on to other things. It happens!\n\nPlease look at the [CONTRIBUTIONS GUIDELINES](./CONTRIBUTING.md)\n\n## Benchmarks\n\nTBD\n\n## License\n\nLicensed under both the [MIT License](./LICENSE-MIT)\n\nCopyright (c) 2023 [Martin Ahindura](https://github.com/tinitto)\n\n## Gratitude\n\n> "...and His (the Father\'s) incomparably great power for us who believe. That power is the same as the mighty strength\n> He exerted when He raised Christ from the dead and seated Him at His right hand in the heavenly realms, \n> far above all rule and authority, power and dominion, and every name that is invoked, not only in the present age but \n> also in the one to come."\n>\n> -- Ephesians 1: 19-21\n\nAll glory be to God.\n\n<a href="https://www.buymeacoffee.com/martinahinJ" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>',
    'author': 'Martin',
    'author_email': 'team.sopherapps@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
