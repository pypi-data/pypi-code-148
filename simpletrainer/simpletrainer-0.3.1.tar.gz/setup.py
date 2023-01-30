# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletrainer',
 'simpletrainer.common',
 'simpletrainer.components',
 'simpletrainer.components.adversarial',
 'simpletrainer.components.basic',
 'simpletrainer.components.debug',
 'simpletrainer.components.grad',
 'simpletrainer.components.lr_scheduler',
 'simpletrainer.components.metric',
 'simpletrainer.components.notification',
 'simpletrainer.components.terminal',
 'simpletrainer.core',
 'simpletrainer.loggers',
 'simpletrainer.utils']

package_data = \
{'': ['*']}

install_requires = \
['accelerate>=0.12.0,<0.13.0',
 'coolname>=1.1.0,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'tensorboard>=2.10.0,<3.0.0',
 'torchinfo>=1.7.0,<2.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'simpletrainer',
    'version': '0.3.1',
    'description': 'Simple PyTorch Trainer',
    'long_description': '# SimpleTrainer\n\nSimple PyTorch Trianer\n',
    'author': 'wangyuxin',
    'author_email': 'wangyuxin@mokahr.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
