# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplepycli']

package_data = \
{'': ['*']}

install_requires = \
['prompt-toolkit>=3.0.36,<4.0.0']

setup_kwargs = {
    'name': 'simplepycli',
    'version': '1.0.0',
    'description': 'A really simple library for interactive python CLIs.',
    'long_description': '# PyCLI\nPyCLI is a really simple library for interactive python CLIs. I mostly built\nit for personal use on side projects, but feel free to use it.\n\n## Install Instructions\nTo install:\n```python\npip install simplepycli\n```\n\n## Basic API Example\nThe API is really simple, so here is a comprehensive example of how it works. This is also available at example.py:\n\n```python\nfrom simplepycli import PyCLIApp\n\n# The only paramater for PyCLIApp is the marker to use in front of the terminal; defaults to "> "\napp = PyCLIApp("> ")\n\n@app.command("egg", "Prints egg to the console")\ndef egg(params):\n  print("egg")\n\n@app.command("echotwice", "Echos the string passed in as a paramater twice")\ndef echotwice(params):\n  for i in range(2):\n    print(params)\n\napp.run()\n```\n\nThis outputs a terminal that behaves like this\n```\n> egg\negg\n> echotwice abc\nabc\nabc\n> help\nexit : Exit the current CLI session and close the program.\nhelp : List available commands and their help messages.\nclear : Clear the current command line.\negg : Prints egg to the console\nechotwice : Echos the string passed in as a paramater twice\n> |\n```\n',
    'author': 'Adithya Yerramsetty',
    'author_email': 'adithyay@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
