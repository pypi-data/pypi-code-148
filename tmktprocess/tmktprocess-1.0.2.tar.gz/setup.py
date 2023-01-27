# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmktprocess']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tmktprocess',
    'version': '1.0.2',
    'description': 'An easyful thread runner',
    'long_description': '# TMKTProcess\n\n## How to install it\n\n```sh\npip install tmktprocess\n```\n\n## How to import it\n\n```py\nfrom tmktprocess import Process\n```\n\n## How to use it\n\n```py\ndef my_func(*args, **kwargs):\n    # do some stuff\n    pass\n```\n\n> To start your process you have to do this:\n\n```py\nprocess = Process(my_func)\nprocess.start(my_args, my_kwargs)\nresult = process.join()\n```\n\n> The .start() will call your function and pass the args and kwargs, then the result will be return with the .join() method\n\n### Use with Event\n\n> You can also pass an Event from ```threading``` package in __init__ call.\n\n```py\nfrom threading import Event\nmy_event = Event()\nprocess = Process(my_func, my_event)\n```\n\n> When the method will end, the event will be set\n> \n> You can use it for everything you want',
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
