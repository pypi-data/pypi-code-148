import sqlite3
import os

from Table import Table


class Database(Table):
    def __init__(self, database_name: str) -> None:
        if database_name not in os.listdir():
            open(database_name, 'w').close()

        self.db_name = database_name
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

# db = Database('db.db')
# db.create_table(table_name='table_name', data_fields={
#     'field1': 'TEXT',
#     'field2': 'INTEGER',
#     'field3': 'NULL'
# })

# db.add_field(table_name='table_name', field_name='field4', field_type='NULL')

# db.insert('table_name',
#           ('field1', 'field2'),
#           ('Tom',    '12'),
#           ('Jake',   '15'))

# db.delete_field('table_name', field_name='field4')

# db.delete_where('table_name', delete_condition="field2=12")

# print(db.get_fields('table_name'))

