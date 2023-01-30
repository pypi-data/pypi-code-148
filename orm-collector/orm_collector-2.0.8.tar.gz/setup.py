# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orm_collector', 'orm_collector.api', 'orm_collector.scripts']

package_data = \
{'': ['*'], 'orm_collector': ['sql/*']}

install_requires = \
['aiomcache>=0.8.0,<0.9.0',
 'basic_logtools>=0.1.7,<0.2.0',
 'click>=8.1.0,<9.0.0',
 'dacite>=1.7.0,<2.0.0',
 'fastapi-cache2[memcache]>=0.2.0,<0.3.0',
 'fastapi>=0.89.1,<0.90.0',
 'geoalchemy2>=0.13.1,<0.14.0',
 'gunicorn>=20.1.0,<21.0.0',
 'networktools>=1.6.0,<2.0.0',
 'psycopg2>=2.9.5,<3.0.0',
 'rich>=13.2.0,<14.0.0',
 'shapely>=2.0.0,<3.0.0',
 'sqlalchemy>=1.4.46',
 'ujson>=5.7.0,<6.0.0',
 'uvicorn>=0.20.0,<0.21.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['orm_create_db = '
                     'orm_collector.scripts.create_db:run_crear_schema',
                     'orm_load_data = '
                     'orm_collector.scripts.load_data:load_data_orm',
                     'orm_show_data = '
                     'orm_collector.scripts.show_data:show_data',
                     'orm_vars = orm_collector.scripts.create_db:show_envvars']}

setup_kwargs = {
    'name': 'orm-collector',
    'version': '2.0.8',
    'description': 'ORM api for collector projects, include a REST API to expose some keys functions',
    'long_description': '# ORM Collector Schemma\n\nEste módulo consiste en la descripción de modelos de tablas\ny sus relaciones, las clases que administran los datos de manera \nsencilla entregando una API, y las herramientas de creación del\nesquema.\n\n# Tecnologías que usa\n\n- Sqlalchemy\n- GeoSqlalchemy\n- Posgresql\n- Python3\n\n# Modo de instalación\n\nPrimero, deberás clonar el proyecto:\n\n~~~\ngit clone http://gitlab.csn.uchile.cl/dpineda/orm_collector.git\n~~~\n\nLuego, instalar en modo develop dentro de tu ambiente\nvirtual\n\n~~~\npython setup.py develop\n~~~\n\n',
    'author': 'David Pineda',
    'author_email': 'dahalpi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
