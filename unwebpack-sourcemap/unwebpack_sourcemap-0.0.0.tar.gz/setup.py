# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['unwebpack_sourcemap']
install_requires = \
['beautifulsoup4==4.7.1',
 'certifi>=2022.12.7',
 'chardet==3.0.4',
 'idna==2.8',
 'requests==2.22.0',
 'soupsieve',
 'urllib3']

entry_points = \
{'console_scripts': ['unwebpack-sourcemap = unwebpack_sourcemap:main']}

setup_kwargs = {
    'name': 'unwebpack-sourcemap',
    'version': '0.0.0',
    'description': "Recovers uncompiled TypeScript sources from Webpack sourcemaps. A fork of rarecoil's work.",
    'long_description': '# unwebpack-sourcemap\n\n### Recover uncompiled TypeScript sources, JSX, and more from Webpack sourcemaps.\n\nThis is a Python command line application that parses Webpack sourcemaps and returns uncompiled TypeScript sources.\n\nunwebpack-sourcemap can process source maps on the local filesystem, or it can discover source maps on a remote website.\n\n## Introduction\nIf you\'re unfamiliar with source maps, you can read:\n* ["Introduction to JavaScript Source Maps"][5] by Google Chrome Developers\n* ["Use a source map"][6] by Firefox Source Docs\n\n## Installation\n#### 1. Create a new Python virtualenv in a directory named `venv`.\n```\npython3 -m venv venv\n```\n\n#### 2. Activate the virtualenv.\n```\nsource venv/bin/activate\n```\n\n#### 3. Install unwebpack-sourcemap from PyPI.\n```\npython3 -m pip install unwebpack-sourcemap\n```\nNote: unwebpack-sourcemap comes with Python dependencies that may conflict with the dependencies in your system installation of Python. That is why it is important to **always install unwebpack-sourcemap inside of a virtualenv,**\nwhich won\'t make any changes to your surrounding system.\n\n#### 4. Try running unwebpack-sourcemap.\n```\nunwebpack-sourcemap --help\n```\n\nThe below examples assume that you are inside of an **activated virtualenv**.\n\nIf you have installed unwebpack-sourcemap in a virtualenv, but want to avoid activating it, you can find the unwebpack-sourcemap command in the location `venv/bin/unwebpack-sourcemap`.\n\n## Usage\nThese examples use the `--make-directory` flag to create a subdirectory named `output_dir`.\nYou can omit the `--make-directory` if you want to use an existing empty directory.\n\n#### Example #1: Unpacking a sourcemap on the local filesystem\n```\nunwebpack-sourcemap --make-directory --local /path/to/source.map output_dir\n```\n\n#### Example #2: Unpacking a sourcemap on a remote website\n```\nunwebpack-sourcemap --make-directory https://pathto.example.com/source.map output_dir\n```\n\n#### Example #3: Unpacking a sourcemap on a remote website (*with autodetection*)\nTo attempt to read all `<script src>` on an HTML page, fetch JS assets, look for `sourceMappingURI`, and pull sourcemaps from remote sources:\n\nThis will:\n1. read all of the `<script src=>` tags on an HTML page\n2. fetch JavaScript assets\n3. look for `sourceMappingURI` and pull the sourcemaps that are found.\n\nTo do this, the command is:\n```\nunwebpack-sourcemap --make-directory --detect https://pathto.example.com/spa_root/ output_dir\n```\n\n## License and credit\nunwebpack-sourcemap was [originally][1] published by [rarecoil][2] under the [MIT license][3]. rarecoil has also published a blog post [explaining the design and functionality][7] of the original version of unwebpack-sourcemap.\n\nThis repository is a fork of unwebpack-sourcemap maintained by [James Mishra][4] and packaged for PyPI.\n\nThis repository is also licensed under the MIT license.\n\n[1]: https://github.com/rarecoil/unwebpack-sourcemap\n[2]: https://github.com/rarecoil\n[3]: https://github.com/rarecoil/unwebpack-sourcemap/blob/master/LICENSE\n[4]: https://github.com/jamesmishra\n[5]: https://developer.chrome.com/blog/sourcemaps/\n[6]: https://firefox-source-docs.mozilla.org/devtools-user/debugger/how_to/use_a_source_map/index.html\n[7]: https://medium.com/@rarecoil/spa-source-code-recovery-by-un-webpacking-source-maps-ef830fc2351d',
    'author': 'James Mishra',
    'author_email': 'j@jamesmishra.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
