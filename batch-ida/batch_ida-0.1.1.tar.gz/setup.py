# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batch_ida']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'batch-ida',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Batch-IDA\n\n需要依赖IDA pro和bindiff\n\n## 测试环境：\n\n+ IDA pro 7.7\n+ bindiff 7\n\n保证IDA Pro可以正常使用，bindiff可以正常解析\n\n## 目标\n\n1. 二进制批量生成idb文件\n2. 使用bindiff批量对比idb文件\n3. 读取比较结果',
    'author': 'ZhengZH',
    'author_email': '41407837+chnzzh@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/chnzzh/batch-ida',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
