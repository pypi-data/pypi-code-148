# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lxdx']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lxdx',
    'version': '0.4.2',
    'description': 'Just an extended Python dict with attribute-accessibility, extra methods, and metadata',
    'long_description': 'lxdx\n====\n\n``lxdx`` is an "extended" Python ``dict`` with attribute-like accessibility.\nOther than the usual ``dict`` operations, functions and methods,\nsome useful functions are incorporated as well.\n\nOnly supports Python 3.9+, due to the usage of the `union operator`_ for ``dict``.\n\nWhy this project?\n-----------------\n* Hobbies and curiosities. Just for the fun of programming.\n* ``dataclass`` is not cut for modelling hierarchical data.\n* Brackets when accessing multi-layer data is too many. `Dot notation`_ may be a cleaner way.\n* Introduce utility functions like ``get_from(path)``, inspired from `JsonPath`_, for programmability.\n* Ability to add metadata to the items.\n\nInstallation\n------------\n``lxdx`` is available in `PyPI <https://pypi.org/project/lxdx>`_, and installable via ``pip``:\n\n.. code-block::\n\n    pip install lxdx\n\n\nExamples\n--------\n.. code-block:: python\n\n    from lxdx import Dixt\n\n    assert Dixt() == {}\n    assert Dixt({1: 1, \'alpha\': \'α\'}) == {1: 1, \'alpha\': \'α\'}\n    assert Dixt(alpha=\'α\', beta=\'β\') == {\'alpha\': \'α\', \'beta\': \'β\'}\n    assert Dixt(alpha=\'α\', beta=\'β\').is_supermap_of({\'beta\': \'β\'})\n\n    # data can be deeply nested\n    data = {\'Accept-Encoding\': \'gzip\', \'metadata\': {\'Content-Type\': \'application/json\'}}\n    dx = Dixt(**data)\n\n    # update dx using the union operator\n    dx |= {\'other\': \'dict or Dixt obj\'}\n\n    # \'Normalise\' the keys to use it as attributes additionally.\n    assert dx[\'Accept-Encoding\'] == dx.accept_encoding\n    del dx.accept_encoding\n    print(dx.metadata.CONTENT_TYPE)\n\n    # Instead of\n    dx[\'a-list\'][1][\'obj-attr\'] = \'value\'\n\n    # Is way cleaner\n    dx.a_list[1].obj_attr = \'value\'\n\n    # Programmatically get values\n    assert dx.a_list[1].obj_attr == dx.get_from(\'$.a_list[1].obj_attr\')\n\n    json_str = \'{"a": "JSON string"}\'\n    assert Dixt.from_json(json_str).json() == json_str\n\nDocumentation\n-------------\nFull documentation is at https://hardistones.github.io/lxdx.\n\nFuture\n------\n``lxdx`` is supposed to be a library of "extended" ``list`` and ``dict``. For now there\'s no use case for the ``list`` extension.\n\n**To be supported**\n\n- User-defined meta specification.\n\nLicense\n-------\nThis project and all its files are licensed under the 3-Clause BSD License.\n\n    Copyright (c) 2021, @github.com/hardistones\n    All rights reserved.\n\n    Redistribution and use in source and binary forms, with or without modification,\n    are permitted provided that the following conditions are met:\n\n    1. Redistributions of source code must retain the above copyright notice, this\n       list of conditions and the following disclaimer.\n\n    2. Redistributions in binary form must reproduce the above copyright notice,\n       this list of conditions and the following disclaimer in the documentation\n       and/or other materials provided with the distribution.\n\n    3. Neither the name of the copyright holder nor the names of its contributors\n       may be used to endorse or promote products derived from this software without\n       specific prior written permission.\n\n    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\n    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\n    ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\n    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\n    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n\n\n.. References\n.. _union operator: https://www.python.org/dev/peps/pep-0584\n.. _dot notation: https://en.wikipedia.org/wiki/Property_(programming)#Dot_notation\n.. _JsonPath: https://github.com/json-path/JsonPath\n',
    'author': 'Hardy Stones',
    'author_email': 'hardistones@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hardistones/lxdx',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
