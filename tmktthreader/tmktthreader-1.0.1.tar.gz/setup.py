# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmktthreader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tmktthreader',
    'version': '1.0.1',
    'description': '',
    'long_description': '# TMKTThreader\n\n## How to install it\n\n```sh\npip install tmktthreader\n```\n\n## How to import it\n\n```py\nfrom tmktthreader import Threader\n```\n\n## How to use it\n\n```py\n@Threader\ndef my_func(*args, **kwargs):\n    # do some stuff\n    pass\n\nmy_func(myargs, mykwargs="")\n```\n\n> your function going to be a thread\n\n> the function call return a Thread from ```threading```. So you can .join() it\n\n```py\nt = my_func(*args, **kwargs)\nt.join()\n```',
    'author': 'ladettanguy',
    'author_email': 'sti2dlab.ladettanguy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
