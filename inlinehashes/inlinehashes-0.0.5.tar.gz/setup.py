# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inlinehashes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0', 'rich>=13.2.0,<14.0.0']

entry_points = \
{'console_scripts': ['inlinehashes = inlinehashes.app:run_cli']}

setup_kwargs = {
    'name': 'inlinehashes',
    'version': '0.0.5',
    'description': 'Hash generator for HTML inline styles and scripts',
    'long_description': 'Inlinehashes\n============\n\nA small tool and library to generate the hashes of inline content that needs to be whitelisted when serving an HTML document\nwith a `Content-Security-Policy <https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP>`_ (because, as the name indicates,\nusing ``unsafe-inline`` is not recommended).\n\nYou provide the HTML content (directly or through a file path/URL) then ``inlinehashes`` will parse the document and provide\nyou with a list of elements that need to be explicitly added to the CSP header/tag.\n\nThe tool can be specially useful for scenarios where you use/include external software solutions in your website or application\n(such as a 3rd party CMS, etc), since it will allow you to detect changes after updates and edit you CSP accordingly.\n\n*Quick note: Always verify the content you are whitelisting and be careful when fetching live website data, since any existing\nXSS code will be included in the results.*\n\n**At the moment this package is still in a very early stage, so it still doesn\'t detect all possible items and the current API\nmight change with future releases.**\n\nInline content that is currently detected:\n\n* ``<script></script>`` tags\n* ``<style></style>`` tags\n* Many event handlers defined in element/tag attributes\n* Styles defined directly in the element/tag using the ``style`` attribute\n\n\nInstallation\n------------\n\nUsing pip you just need to ``pip install inlinehashes``\n\nUsage\n-----\n\nThe package can be used through 2 different ways, either by using the CLI interface or programmatically in your python project.\nBellow you can find a quick summary of the available functionality.\n\nCLI app\n.......\n\nThis is the available functionality:\n\n.. code::\n\n  usage: inlinehashes [-h] [-a {sha256,sha384,sha512}] [-o {table,json,plain}] [-t {all,script-src,style-src}] source\n\n  positional arguments:\n    source                URL or local HTML file to check\n\n  options:\n    -h, --help            show this help message and exit\n    -a {sha256,sha384,sha512}, --alg {sha256,sha384,sha512}\n                          Hash algorithm to use (default: sha256)\n    -o {table,json,plain}, --output {table,json,plain}\n                          Format used to write the output (default: table)\n    -t {all,script-src,style-src}, --target {all,script-src,style-src}\n                          Target inline content to look for (default: all)\n\nHere is an example of the output:\n\n.. code::\n\n    $inlinehashes https://ovalerio.net -a sha384 -o json\n    [\n      {\n        "content": "\\n      html {\\n        height: 100%;\\n      }\\n      ",\n        "hash": "sha384-Ku20lQH5qbr4EDPzXD2rf25rEHJNswNYRUNMPjYl7jCe0eHJYDe0gFdQpnKkFUTv",\n        "directive": "style-src",\n        "line": 12,\n        "position": 0\n      }\n    ]\n\n\nLibrary\n.......\n\nHere is the same example, but using python\'s shell:\n\n.. code:: python\n\n    >>> import requests\n    >>> import inlinehashes\n    >>> content = requests.get("https://ovalerio.net").text\n    >>> inlines = inlinehashes.parse(content)\n    >>> inlines\n    [Inline(line=\'17\', position=\'0\')]\n    >>> first = inlines[0]\n    >>> first.short_content\n    \'\\n      html {\\n        height: 100%;\\n      }\\n      \'\n    >>> first.sha256\n    \'sha256-aDiwGOuSD1arNOxmHSp89QLe81yheSUQFjqpWHYCpRY=\'\n    >>> first.sha384\n    \'sha384-Ku20lQH5qbr4EDPzXD2rf25rEHJNswNYRUNMPjYl7jCe0eHJYDe0gFdQpnKkFUTv\'\n    >>> first.sha512\n    \'sha512-cBO6RNy87Tx3HmpXRZUs/DPxGq9ZOqIZ9cCyDum0kNZeLEWVvW5DtYFRmHcQawnAoWeeRmll4aJeLXTb2OLBlA==\'\n    >>> first.content\n    \'\\n      html {\\n        height: 100%;\\n      }\\n      body {\\n        background-image: url("data:image/png;base64,iVBORw0KGgoAAAANS...\'\n\nContributions\n-------------\n\nAll contributions and improvements are welcome.\n',
    'author': 'Gonçalo Valério',
    'author_email': 'gon@ovalerio.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dethos/inlinehashes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
