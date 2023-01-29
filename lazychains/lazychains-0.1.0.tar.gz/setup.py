# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lazychains']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lazychains',
    'version': '0.1.0',
    'description': 'Singly linked lists with incremental instantiation of iterators',
    'long_description': '# lazychains\n\nA Python library to provide "chains", which are Lisp-like singly linked lists \nthat support the lazy expansion of iterators. For example, we can construct a \nChain of three characters from the iterable "abc" and it initially starts as \nunexpanded, shown by the three dots:\n\n.. code:: python\n\n   >>> from lazychains import lazychain\n   >>> c = lazychain( "abc")\n   >>> c\n   chain([...])\n\nWe can force the expansion of *c* by performing (say) a lookup or by forcing the whole\nchain of items by calling expand:\n\n.. code:: python\n\n   >>> c[1]                   # Force the expansion of the next 2 elements.\n   True\n   >>> c\n   chain([\'a\',\'b\',...])\n   >>> c.expand()             # Force the expansion of the whole chain.\n   chain([\'a\',\'b\',\'c\'])\n\nAs we will see, chains are generally less efficient than ordinary arrays. So,\nas a default you should definitely carry on using ordinary arrays and tuples\nmost of the time. But they have a couple of special features that makes them the \nperfect choice for some problems.\n\n   * Chains are immutable and hence can safely share their trailing segments.\n   * Chains can make it easy to work with extremely large (or infinite) \n     sequences.\n\nExpanded or Unexpanded\n----------------------\n\nWhen you construct a chain from an iterator, you can choose whether or not\nit should be immediately expanded by calling chain rather than lazychain.\nThe difference between the two is pictured below. First we can see what happens\nin the example given above where we create the chain using lazychain on \n"abc".\n\nIMAGE GOES HERE\n\nBy contrast, we would immediately go to a fully expanded chain if we were to\nsimply apply chain:\n\n.. code:: python\n\n   >>> from lazychains import chain\n   >>> c = chain( "abc" )\n   >>> c\n   chain([\'a\',\'b\',\'c\'])\n   >>> \n\n\nIMAGE GOES HERE\n',
    'author': 'Stephen Leach',
    'author_email': 'sfkleach@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lazylinks.readthedocs.io/en/latest/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
