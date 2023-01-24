# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_filterset']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy[asyncio]>=1.4,<2']

setup_kwargs = {
    'name': 'sqlalchemy-filterset',
    'version': '1.0.1',
    'description': 'An easy way to filter, sort, paginate SQLAlchemy queries',
    'long_description': '<span style="font-size: 65px; color: #7e56c2">**SQLAlchemy Filterset**</span>\n\n<p align="left">\n    <em>An easy way to filter, sort, paginate SQLAlchemy queries</em>\n</p>\n\n[![codecov](https://codecov.io/gh/sqlalchemy-filterset/sqlalchemy-filterset/branch/main/graph/badge.svg)](https://codecov.io/gh/sqlalchemy-filterset/sqlalchemy-filterset)\n[![CodeQL](https://github.com/sqlalchemy-filterset/sqlalchemy-filterset/actions/workflows/codeql.yml/badge.svg)](https://github.com/sqlalchemy-filterset/sqlalchemy-filterset/actions/workflows/codeql.yml)\n\n\n---\n**Documentation**: <a href="https://sqlalchemy-filterset.github.io/sqlalchemy-filterset/" target="_blank">https://sqlalchemy-filterset.github.io/sqlalchemy-filterset</a>\n\n**Source Code**: <a href="https://github.com/sqlalchemy-filterset/sqlalchemy-filterset" target="_blank">https://github.com/sqlalchemy-filterset/sqlalchemy-filterset</a>\n\n---\nThe library provides a convenient and organized way to filter your database records.\nBy creating a `FilterSet` class, you can declaratively define the filters you want to apply to your `SQLAlchemy` queries.\nThis library is particularly useful in web applications, as it allows users to easily search, filter, sort, and paginate data.\n\nThe key features are:\n\n* [X] Declaratively define filters.\n* [X] Keep all of your filters in one place, making it easier to maintain and change them as needed.\n* [X] Construct complex filtering conditions by combining multiple simple filters.\n* [X] It offers a standard approach to writing database queries.\n* [X] Reduce code duplication by reusing the same filters in multiple places in your code.\n* [X] Sync and Async support of modern SQLAlchemy.\n\n## Installation\n\n```bash\npip install sqlalchemy-filterset\n```\nRequirements: `Python 3.7+` `SQLAlchemy 1.4+`\n\n\n## Basic Usage\n\nThe declarative style allows users to easily specify criteria for filtering the records that are\nreturned from the database by simply setting the attributes of the `ProductFilterSet` class.\nThis can be more convenient and easier to understand than writing raw SQL queries, which\ncan be more error-prone and difficult to maintain.\n\n### Define a FilterSet\n\nIn a declarative style, we describe the attributes that will participate in filtering the query in the database:\n```python\nfrom sqlalchemy_filterset import FilterSet, Filter, RangeFilter, BooleanFilter\n\nfrom myapp.models import Product\n\n\nclass ProductFilterSet(FilterSet):\n    id = Filter(Product.id)\n    price = RangeFilter(Product.price)\n    is_active = BooleanFilter(Product.is_active)\n```\n### Define a FilterSchema\n```python\nimport uuid\nfrom pydantic import BaseModel\n\n\nclass ProductFilterSchema(BaseModel):\n    id: uuid.UUID | None\n    price: tuple[float, float] | None\n    is_active: bool | None\n```\n\n### Usage\n```python\n# Connect to the database\nengine = create_engine("postgresql://user:password@host/database")\nBase.metadata.create_all(bind=engine)\nSessionLocal = sessionmaker(bind=engine)\nsession = SessionLocal()\n\n# Create the filterset object\nfilter_set = ProductFilterSet(session, select(Product))\n\n# Define the filter parameters\nfilter_params = ProductFilterSchema(\n    price=(10, 100),\n    is_active=True,\n)\n\n# Apply the filters to the query\nfiltered_products = filter_set.filter(filter_params)\n```\n#### This example will generate the following query:\n```sql\nSELECT product.id, product.title, product.price, product.is_active\nFROM product\nWHERE product.price >= 10\n  AND product.price <= 100\n  AND product.is_active = true\n```\n\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Andrey Matveev',
    'author_email': 'ra1ze.matveev@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
