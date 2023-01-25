# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['flake8_fastapi_route_case']
install_requires = \
['importlib-metadata>=6.0.0']

entry_points = \
{'flake8.extension': ['FRC = flake8_fastapi_route_case:Plugin']}

setup_kwargs = {
    'name': 'flake8-fastapi-route-case',
    'version': '0.1.0',
    'description': 'Flake8 extension to check FastAPI routes all use the same case',
    'long_description': '# Flake8 FastAPI Route Case\n\nA Flake8 FastAPI plugin to ensure all FastAPI routes follow the same case.\n\n## Rationale\n\nIn a project, you may have many FastAPI endpoints, this plugin will ensure\nall FastAPI routes follow the same case so you don\'t end up with mismatched\ncase.\n\n```python\n@router.get("/users/user_info")\ndef get_user_info():\n    ...\n\n# should be /users/user_info to follow naming convention\n@router.post("/users/userInfo")\ndef post_user_info():\n    ...\n```\n',
    'author': 'Harry Lees',
    'author_email': 'harry.lees@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1',
}


setup(**setup_kwargs)
