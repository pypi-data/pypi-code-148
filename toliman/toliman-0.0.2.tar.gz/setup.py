# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['toliman']

package_data = \
{'': ['*']}

install_requires = \
['astroquery>=0.4.6,<0.5.0',
 'dLux>=0.9',
 'jax>=0.4.1',
 'opt-einsum>=3.3.0,<4.0.0',
 'pysynphot>=2.0.0']

setup_kwargs = {
    'name': 'toliman',
    'version': '0.0.2',
    'description': 'A differential model of TOLIMAN telescope.',
    'long_description': 'TOLIMAN\n=======\nThe goal of the TOLIMAN mission is to answer the question: is there a planet\naround Alpha Centauri? The critical advance represented by the TOLIMAN \ntelescope is its ability to assess a specific star. Until now telescopes have\nbeen designed to survey many stars and confirm (with biases) which ones may \nhave exoplanets. None have chosen a star and tried to resolutely and without \nquestion find all and any exoplanets in orbit. \n',
    'author': 'Jordan Dennis',
    'author_email': 'jdenn105@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
