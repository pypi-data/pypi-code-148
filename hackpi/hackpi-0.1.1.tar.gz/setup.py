# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hackpi']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.89.1,<0.90.0',
 'pydantic>=1.10.4,<2.0.0',
 'sqlalchemy>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'hackpi',
    'version': '0.1.1',
    'description': 'HackPi - is a library for the FastAPI framework that adds additional functionality that simplifies development.',
    'long_description': "# HackPi\n\nHackPi - is a library for the FastAPI framework that adds additional functionality that simplifies development. \n\n## Introduction\n### Features:\n- Генерация endpoints по моделям SQLAlchemy и Pydantic\n- Самая простая генерация JWT-токенов\n- Отправка писем с кодом активации/восстановления на почту\n- Двухфакторная аутентификация используя TOTP\n- Готовые методы регистрации, авторизации\n- Система ролей с возможностью ограничения доступа\n\nБиблиотека может использоваться для быстрого прототипирования бекенда, либо для построения функционала для хакатонов.\n\n### Installing\nЧтобы установить библиотеку, выполните в терминале простую команду:\n```bash\npip3 install hackpi\n```\n\nЧтобы проверить наличие библиотеки на компьютере, нужно ввести следующую команду:\n```bash\npip3 list\n```\nИ в выведенном вы увидите библиотеку hackpi с текущей версией (актуальная - 0.1.1).\n\nУра! Теперь вы можете пользоваться всеми возможностями HackPi.\n\n## Usage\n## Подключение к базе данных\nДля подключения к базе данных используется класс `Database`. При содании объекта этого класса, нужно передать в конструктор расположение SQLite3 базы данных. Пока что HackPi может работать только с этой базой данных.\n```python\n# db.py\nfrom hackpi.Database import Database\n\ndb = Database('sqlite:///database.sqlite3')\n```\n\nВ последствии, мы можем передавать объект `db` в другие методы, которые будут записывать информацию в базу данных.\n\n## Модели SQLAlchemy и Pydantic\nВ этом туториале вы увидите работу библиотеки на примере работы с пользователем. Нам всегда необходимо иметь две модели: модель SQLAlchemy и модель Pydantic. \n\n```python\n# models.py\nfrom hackpi.Database import Base\nfrom sqlalchemy import Column, Integer, String\nfrom db import db\n\nclass User(Base):\n\t__tablename__ = 'users'\n\n\tid: int = Column(Integer, primary_key=True)\n\temail: str = Column(String, unique=True)\n\tpassword: str = Column(String)\n\ndb.create_all()\n```\n\nРазберем файл `models.py`. Мы создали модель SQLAlchemy, наследовав ее от `Base`. Название таблицы - `users`. Таблица имеет следующие столбцы: `id`, `email`, `password`. Затем, мы вызвали метод для создания таблицы в базе данных.\n\n```python\n# schemas.py\nfrom pydantic import BaseModel\n\nclass User(BaseModel):\n\temail: str\n\tpassword: str\n```\n\nМы создали простую схему Pydantic, которая содержит в себе только `email` и `password`.\n\n## Создание роутеров\nИтак, чтобы сгенерировать эндпоинты, используя модели SQLAlchemy и Pydantic, необходимо создать `main.py` файл, и написать в нем следующее:\n```python\n# main.py\nfrom fastapi import FastAPI\nfrom hackpi.Router import Router\nfrom models import User as UserModel\nfrom schemas import User as UserSchema\nfrom db import db\n\napp = FastAPI()\n\nrouter = Router(db, UserModel, UserSchema)\n\napp.include_router(router.get_router())\n```\n\nВведя команду `uvicorn main:app --reload` в терминал, запустится бекенд. Можно перейти в документацию, и увидеть результат генерации эндпоинтов.",
    'author': 'thenesterov',
    'author_email': 'thenesterov@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thenesterov/hackpi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
