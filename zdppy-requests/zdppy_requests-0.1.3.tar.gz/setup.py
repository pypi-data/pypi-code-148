# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zdppy_requests',
 'zdppy_requests.certifi',
 'zdppy_requests.charset_normalizer',
 'zdppy_requests.charset_normalizer.assets',
 'zdppy_requests.charset_normalizer.cli',
 'zdppy_requests.idna',
 'zdppy_requests.urllib3',
 'zdppy_requests.urllib3.contrib',
 'zdppy_requests.urllib3.contrib._securetransport',
 'zdppy_requests.urllib3.packages',
 'zdppy_requests.urllib3.packages.backports',
 'zdppy_requests.urllib3.util']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zdppy-requests',
    'version': '0.1.3',
    'description': '',
    'long_description': '# zdppy_requests\n基于requests二开的HTTP请求库，无任何第三方依赖，可独立使用，不受开源框架迭代的影响。\n\n\n# 使用示例\n## 安装\n```bash\npip install zdppy_requests\n```\n\n## 获取网页源码\n```python\nimport zdppy_requests as zr\n\nresponse = zr.get("https://www.baidu.com/")\nprint(response.status_code)\nprint(response.text)\n\n创建Mapping\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nbody = {\n  "mappings": {\n    "properties": {\n      "name": {\n        "type": "text"\n      },\n      "price": {\n        "type": "double"\n      },\n      "author": {\n        "type": "text"\n      },\n      "pub_date": {\n        "type": "date"\n      }\n    }\n  }\n}\nindex = "books"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\n\nresponse = zr.put(f"{url}/{index}", json=body, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n## 查询Mapping\n```python\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nindex = "books/_mapping?pretty"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\ntarget = f"{url}/{index}"\n\nresponse = zr.get(target, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n## 删除Mapping\n```python\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nindex = "books"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\ntarget = f"{url}/{index}"\n\nresponse = zr.delete(target, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n## 根据ID新增数据\n```python\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nindex = "books/_doc"\ndid = "1"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\ntarget = f"{url}/{index}/{did}"\nbody = {\n\t"name": "《JavaScript全栈开发实战》",\n\t"author": "张大鹏",\n\t"price": 123,\n\t"pub_date": "2019-12-12"\n}\n\nresponse = zr.put(target, json=body, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n## 根据ID查询图书\n```python\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nindex = "books/_doc"\ndid = "1"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\ntarget = f"{url}/{index}/{did}"\n\nresponse = zr.get(target, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n## 根据ID删除图书\n```python\nimport zdppy_requests as zr\nfrom zdppy_requests.auth import HTTPBasicAuth\n\nurl = "http://localhost:9200"\nindex = "books/_doc"\ndid = "1"\nauth = HTTPBasicAuth(\'elastic\',\'zhangdapeng520\')\ntarget = f"{url}/{index}/{did}"\n\nresponse = zr.delete(target, auth=auth)\nprint(response.status_code)\nprint(response.text)\n```\n\n\n',
    'author': 'zhangdapeng520',
    'author_email': '1156956636@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
