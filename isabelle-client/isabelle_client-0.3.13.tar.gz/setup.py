# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['isabelle_client']

package_data = \
{'': ['*'], 'isabelle_client': ['resources/*']}

extras_require = \
{':python_version < "3.9"': ['importlib-resources']}

setup_kwargs = {
    'name': 'isabelle-client',
    'version': '0.3.13',
    'description': 'A client to Isabelle proof assistant server',
    'long_description': '|Binder|\\ |PyPI version|\\ |Anaconda version|\\ |CircleCI|\\ |Documentation Status|\\ |codecov|\n\nPython client for Isabelle server\n=================================\n\n``isabelle-client`` is a TCP client for\n`Isabelle <https://isabelle.in.tum.de>`__ server. For more information\nabout the server see part 4 of `the Isabelle system\nmanual <https://isabelle.in.tum.de/dist/Isabelle2021-1/doc/system.pdf>`__.\n\nHow to Install\n==============\n\nThe best way to install this package is to use ``pip``:\n\n.. code:: sh\n\n   pip install isabelle-client\n\n\nAnother option is to use Anaconda:\n\n.. code:: sh\n\t  \n   conda install -c conda-forge isabelle-client \n\nOne can also download and run the client together with Isabelle in a\nDocker contanier:\n\n.. code:: sh\n\n   docker build -t isabelle-client https://github.com/inpefess/isabelle-client.git\n   docker run -it --rm -p 8888:8888 isabelle-client jupyter-lab --ip=0.0.0.0 --port=8888\n\nHow to use\n==========\n\n.. code:: python\n\n   from isabelle_client import get_isabelle_client, start_isabelle_server\n   \n   # start Isabelle server\n   server_info, _ = start_isabelle_server()\n   # create a client object\n   isabelle = get_isabelle_client(server_info)\n   # send a theory file from the current directory to the server\n   response = isabelle.use_theories(\n       theories=["Example"], master_dir=".", watchdog_timeout=0\n   )\n   # shut the server down\n   isabelle.shutdown()\n\n\nFor more details, follow the `usage\nexample <https://isabelle-client.readthedocs.io/en/latest/usage-example.html#usage-example>`__\nfrom documentation, run the\n`script <https://github.com/inpefess/isabelle-client/blob/master/examples/example.py>`__,\nor use ``isabelle-client`` from a\n`notebook <https://github.com/inpefess/isabelle-client/blob/master/examples/example.ipynb>`__,\ne.g.\xa0with\n`Binder <https://mybinder.org/v2/gh/inpefess/isabelle-client/HEAD?labpath=isabelle-client-examples/example.ipynb>`__ (Binder might fail with \'Failed to create temporary user for ...\' error which is `well known <https://mybinder-sre.readthedocs.io/en/latest/incident-reports/2018-02-20-jupyterlab-announcement.html>`__ and related neither to ``isabelle-client`` nor to the provided ``Dockerfile``. If that happens, try to run Docker as described in the section above).\n\nMore documentation\n==================\n\nMore documentation can be found\n`here <https://isabelle-client.readthedocs.io/en/latest>`__.\n\nSimilar Packages\n================\n\nThere are Python clients to other interactive theorem provers, for\nexample:\n\n* `for Lean\n  <https://github.com/leanprover-community/lean-client-python>`__\n* `for Coq <https://github.com/IBM/pycoq>`__\n* `another one for Coq <https://github.com/ejgallego/pycoq>`__\n\nModules helping to inetract with Isabelle server from Python are\nparts of the `Proving for Fun\n<https://github.com/maxhaslbeck/proving-contest-backends>`__ project.\n\nHow to cite\n===========\n\nIf you’re writing a research paper, you can cite Isabelle client\nusing the `following DOI\n<https://doi.org/10.1007/978-3-031-16681-5_24>`__. You can also cite\nIsabelle 2021 (and the earlier version of the client) with `this\nDOI <https://doi.org/10.1007/978-3-030-81097-9_20>`__.\n\nHow to Contribute\n=================\n\nPlease follow `the contribution guide <https://isabelle-client.readthedocs.io/en/latest/contributing.html>`__ while adhering to `the code of conduct <https://isabelle-client.readthedocs.io/en/latest/code-of-conduct.html>`__.\n\n\n.. |PyPI version| image:: https://badge.fury.io/py/isabelle-client.svg\n   :target: https://badge.fury.io/py/isabelle-client\n.. |Anaconda version| image:: https://anaconda.org/conda-forge/isabelle-client/badges/version.svg\n   :target: https://anaconda.org/conda-forge/isabelle-client\n.. |CircleCI| image:: https://circleci.com/gh/inpefess/isabelle-client.svg?style=svg\n   :target: https://circleci.com/gh/inpefess/isabelle-client\n.. |Documentation Status| image:: https://readthedocs.org/projects/isabelle-client/badge/?version=latest\n   :target: https://isabelle-client.readthedocs.io/en/latest/?badge=latest\n.. |codecov| image:: https://codecov.io/gh/inpefess/isabelle-client/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/inpefess/isabelle-client\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/inpefess/isabelle-client/HEAD?labpath=isabelle-client-examples/example.ipynb\n',
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/inpefess/isabelle-client',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
