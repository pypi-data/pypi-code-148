# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_scrapy',
 'jsw_scrapy.helpers',
 'jsw_scrapy.models',
 'jsw_scrapy.pipelines',
 'jsw_scrapy.spiders']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'jsw-nx>=1.0.110,<2.0.0',
 'oss2>=2.16.0,<3.0.0',
 'psutil>=5.9.0,<6.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0']

setup_kwargs = {
    'name': 'jsw-scrapy',
    'version': '1.0.14',
    'description': 'Jsw for scrapy.',
    'long_description': '# jsw-scrapy\n> Jsw for scrapy.\n\n## installation\n- https://pypi.org/project/jsw-scrapy/\n```shell\npip install jsw-scrapy -U\n```\n\n## usage\n```python\nfrom jsw_scrapy.spiders.base_spider import BaseSpider\nfrom jsw_scrapy.pipelines.base_pipeline import BasePipeline\n```\n',
    'author': 'feizheng',
    'author_email': '1290657123@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://js.work',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
