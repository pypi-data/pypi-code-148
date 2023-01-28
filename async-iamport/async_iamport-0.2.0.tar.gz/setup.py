# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_iamport']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3,<4.0.0', 'arrow>=1.2.3,<2.0.0']

setup_kwargs = {
    'name': 'async-iamport',
    'version': '0.2.0',
    'description': '',
    'long_description': '# IAMPORT async python rest client\n\nfrom https://github.com/iamport/iamport-rest-client-python\n\n## 개선 사항\n1. sync -> async\n2. Token 재사용\n   - 만료 60s 이상 남았을 경우 재사용\n   - 그 이하일 경우 재인증\n3. .format() -> f-string\n4. typing 적용, mypy 적용\n\n\n## 변경 사항\n1. python2 지원 안함\n2. requests -> aiohttp\n3. 기존 retry(3회) 옵션 제거\n\n## 작업 예정\n1. 필수 필드 검증을 아에 제거하고 iamport api 의 응답만 확인하도록 해서 필드 변경에 대한 유연성 및 코드의 책임 범위를 낮추기\n   - 기존 method 호환을 위해 유지\n   - 추가 API는 path parameter 만 positional args 으로 처리, 나머지는 kwargs로 payload 담음\n2. ~~함수들의 이름을 iamport api들의 호출 이름과 유사하게 전부 정리하기~~\n   - 기존 client api 유지\n3. 미구현 API 추가 예정\n   - param validation 제거\n   - type annotation 추가\n   - docstring 추가\n\n## 주의 사항\n- 사용 중 발생한 문제의 책임은 사용자에게 있습니다.\n- iamport 정식 api로 동작 완전성 테스트 되지 않았습니다. url 이상 여부만 검증 되었습니다.\n\n\n## Deps\n\n- python >= 3.7\n\n- Aiohttp >= 3.8.3\n- arrow >= 1.2.3\n\n\n## Install\n\n```commandline\npip install async-iamport\n```\n\n## FastAPI Example\n\n```python\nfrom fastapi import FastAPI\n\nfrom async_iamport import AsyncIamport\n\nDEFAULT_TEST_IMP_KEY = "imp_apikey"\nDEFAULT_TEST_IMP_SECRET = (\n    "ekKoeW8RyKuT0zgaZsUtXXTLQ4AhPFW3ZGseDA6b"\n    "kA5lamv9OqDMnxyeB9wqOsuO9W3Mx9YSJ4dTqJ3f"\n)\n\nasync_iamport = AsyncIamport(\n    imp_key=DEFAULT_TEST_IMP_KEY, imp_secret=DEFAULT_TEST_IMP_SECRET\n)\n\napp = FastAPI(on_shutdown=[async_iamport.close_session])\n\n\nmocked_response = {\n    "status": "paid",\n    "amount": 1000,\n}\n\n@app.get("/")\nasync def root():\n    return await async_iamport.find_by_merchant_uid(merchant_uid="1234qwer")\n```\n```commandline\nuvicorn main:app --reload\n``` \n',
    'author': '한바름',
    'author_email': 'rumbarum@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
