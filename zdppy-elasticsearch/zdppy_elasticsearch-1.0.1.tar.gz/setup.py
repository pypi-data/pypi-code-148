# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_elasticsearch']

package_data = \
{'': ['*']}

install_requires = \
['zdppy-requests>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'zdppy-elasticsearch',
    'version': '1.0.1',
    'description': 'python操作ElasticSearch的基础组件',
    'long_description': '# zdppy_elasticsearch库使用\n项目地址\nGitHub开源地址：https://github.com/zhangdapeng520/zdppy_elasticsearch\n\n主要看dev分支的代码。\n\n# 版本历史\n- 2023/01/30 v1.0.1 使用zdppy_requests完全重构项目\n\n# 快速入门\n## 安装\n```bash\npip install zdppy_elasticsearch\n```\n\n## 创建Mapping\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nbody = {\n  "mappings": {\n    "properties": {\n      "name": {\n        "type": "text"\n      },\n      "price": {\n        "type": "double"\n      },\n      "author": {\n        "type": "text"\n      },\n      "pub_date": {\n        "type": "date"\n      }\n    }\n  }\n}\nindex = "books"\nprint(es.add_mapping(index, body))\n```\n\n## 查询Mapping\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\nprint(es.get_mapping(index))\n```\n\n## 删除Mapping\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\nprint(es.delete_index(index))\n```\n\n## 根据ID新增数据\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\ndid = 1\nbody = {\n\t"name": "《JavaScript全栈开发实战》",\n\t"author": "张大鹏",\n\t"price": 123,\n\t"pub_date": "2019-12-12"\n}\nprint(es.add(index, did, body))\n```\n\n## 根据ID查询图书\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\ndid = 1\nprint(es.get(index, did))\nprint(es.get(index, did, is_source=True))\n```\n\n## 根据ID删除图书\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\ndid = 1\nprint(es.delete(index, did))\nprint(es.get(index, did, is_source=True))\n```\n\n## 批量插入数据\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\ndata = [\n\t{"index": {"_index": "books", "_type" : "_doc", "_id" : "1"}},\n\t{"name": "《JavaScript全栈开发实战》", "author": "张大鹏", "price": 123, "pub_date": "2019-12-12" },\n\t{"index": {"_index": "books", "_type" : "_doc", "_id" : "2"}},\n\t{"name": "《React学习手册》", "author": "张大鹏", "price": 122, "pub_date": "2019-12-12" },\n\t{"index": {"_index": "books", "_type" : "_doc", "_id" : "3",}},\n\t{"name": "《精通Go语言》", "price": 128, "pub_date": "2019-12-12" }\n]\n\ndata1 = [\n\t{"name": "《JavaScript全栈开发实战》", "author": "张大鹏", "price": 123, "pub_date": "2019-12-12" },\n\t{"name": "《React学习手册》", "author": "张大鹏", "price": 122, "pub_date": "2019-12-12" },\n\t{"name": "《精通Go语言》", "price": 128, "pub_date": "2019-12-12" }\n]\n\n\n# 自定义索引和和ID\nprint(es.add_many(data))\n\n# 自动生成ID\nprint(es.add_many(data1, index=index))\n```\n\n## 搜索所有图书\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\n\n# 搜索所有图书\nprint(es.search(index))\n```\n\n## 搜索特定价格范围的图书\n```python\nimport zdppy_elasticsearch as ze\n\nes = ze.ElasticSearch(password="zhangdapeng520")\nindex = "books"\nquery = {\n  "query": {\n    "range": {\n      "price": {\n        "gt": 123,\n        "lte": 130\n      }\n    }\n  }\n}\n\n# 搜索所有图书\nprint(es.search(index, query))\n```',
    'author': '张大鹏',
    'author_email': '1156956636@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zhangdapeng520/zdppy_elasticsearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
