# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mysqlite']
setup_kwargs = {
    'name': 'mysqlite',
    'version': '0.1.0',
    'description': "mysqlite.Database('database_name.db')",
    'long_description': '# ISQLITE\n___\n# About\n\nThis library was created to simplify the handling of .db, .sqlite, .sqlite3 files\nin small python projects.\nFor example, if you want to write something quickly without bothering with SQL queries.\n___\n# Start\nConnecting an existing one or creating a new database file\n`db = isqlite.Database(\'database_filename.db\')`\n\n___\n# Create table\nCreate a new table and fields\n```\ndb.create_table(table_name=\'table_name\', data_fields={\n    \'field1\': \'TEXT\',\n    \'field2\': \'INTEGER\',\n    \'field3\': \'NULL\'\n})\n```\nDatabase:\n| field1 | field2 | field3 |\n| -------|--------|--------|\n\n___\n# Add new field\n`db.add_field(table_name=\'table_name\', field_name=\'field4\', field_type=\'NULL\')`\nDatabase:\n| field1 | field2 | field3 | field4 |\n| -------|--------|--------|--------|\n\n___\n# Add data - insert\n```\ndb.insert(\'table_name\',\n          (\'field1\', \'field2\'),\n          (\'Tom\',    \'12\'),\n          (\'Jake\',   \'15\'))\n```\nDatabase:\n| field1 | field2 | field3 | field4 |\n| -------|--------|--------|--------|\n| Tom    | 12     | NULL   | NULL   |\n| jake   | 15     | NULL   | NULL   |\n\n___\n# Delete field\n`db.delete_field(\'table_name\', field_name=\'field4\')`\nDatabase:\n| field1 | field2 | field3 |\n| -------|--------|--------|\n| Tom    | 12     | NULL   |\n| jake   | 15     | NULL   |\n\n___\n# Delete where\n`db.delete_where(\'table_name\', delete_condition="field2=12")`\nDatabase:\n| field1 | field2 | field3 |\n| -------|--------|--------|\n| jake   | 15     | NULL   |\n\n___\n# Get fields\n`print(db.get_fields(\'table_name\'))`\nOutput:\n> [(0, \'field1\', \'TEXT\', 0, None, 0), (1, \'field2\', \'INT\', 0, None, 0), (2, \'field3\', \'\', 0, None, 0)]\n\n',
    'author': 'Django-B',
    'author_email': 'django.ppp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
