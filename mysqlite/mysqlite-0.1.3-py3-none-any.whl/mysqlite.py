import sqlite3
import os

class Data:
    """Data interaction"""
    def insert(self, table_name: str, fields: list, *values: list) -> None:
        """insert("table_name", (field1, field2), ("Tom", 12), ("Jake", 15), (...), ...)"""
        print(values)
        converted_values = []
        for j in values:
            lst = []
            for i in j:
                if isinstance(i, str):
                    i = f"'{i}'"
                lst.append(i)
            converted_values.append(lst)
                

        print(converted_values)

        cmd_fields = ', '.join(fields)
        cmd_values = ', '.join(map(str, ['('+str(x[0])+', '+str(x[1])+')' for x in converted_values]))
        print(cmd_values)

        command = f"INSERT INTO {table_name} ({cmd_fields}) VALUES {cmd_values};"
        print(command)

        self.execute_cmd(command)

    def delete_where(self, table_name: str, delete_condition: str) -> None:
        """
        delete_where(table_name="table1", delete_condition="company='Huawei'")
        used: DELETE FROM product WHERE company='Huawei';
        """
        delete_command = f'DELETE FROM {table_name} WHERE {delete_condition};'

        self.execute_cmd(delete_command)


class Table(Data):
    """Basic operations with database tables"""
    def create_table(self, table_name: str, data_fields: dict) -> None:
        """
        data_fields = {
            'field1_name': 'INTEGER',
            'field2_name': 'NULL',
        }
        
        Field types:
            NULL —  NULL:
 
            INTEGER — integer type;

            REAL — real type;

            TEXT — string type;

            BLOB — binary data, stored as is (such as images);
        """
        
        fields = [x[0]+' '+x[1]+',\n' for x in data_fields.items()]
        fields = ''.join(fields).strip()[:-1]

        command = f"""CREATE TABLE IF NOT EXISTS {table_name}(
            {fields}
        )"""
        # print(command)
        
        self.execute_cmd(command)

    def rename_table(self, table_old_name: str, table_new_name: str) -> None:
        """Rename Table"""
        command = f'''ALTER TABLE {table_old_name}
            RENAME TO {table_new_name};'''
        self.execute_cmd(command)

    def add_field(self, table_name, field_name: str, field_type: str) -> None:
        """
        Field types:
            NULL —  NULL:
            
            INTEGER — integer type;
            
            REAL — real type;
            
            TEXT — string type;

            BLOB — binary data, stored as is (such as images);
        """
        command = f'''ALTER TABLE {table_name} ADD COLUMN {field_name} {field_type}'''
        self.execute_cmd(command)

    def delete_field(self, table_name: str, field_name: str) -> None:
        """Deleting a column"""

        fields = self.get_fields(table_name)
        cmd_data = [x[1] for x in fields if x[1]!=field_name]
        cmd_string = ', '.join(cmd_data)
        # print(cmd_string)
        
        copy_table_cmd = f'CREATE TABLE backup AS SELECT {cmd_string} FROM {table_name};'
        drop_table_cmd = f'DROP TABLE {table_name};'
        rename_table_cmd = f'ALTER TABLE backup RENAME TO {table_name};'

        self.execute_cmd(copy_table_cmd)
        self.execute_cmd(drop_table_cmd)
        self.execute_cmd(rename_table_cmd)
        

    def clear_table(self, table_name: str) -> None:
        """Complete deletion of data, clearing the table"""
        command = f'DELETE FROM {table_name};'
        self.execute_cmd(command)

    # def backup_table(self, existing_table_name: str, for_backup_table_name: str) -> None:

    def delete_table(self, table_name: str) -> None:
        """Delete Table"""
        command = f'DROP TABLE {table_name};'
        self.execute_cmd(command)

    def get_fields(self, table_name: str) -> str:
        """The information is returned as a tuple
        [(
            column index,

            column name,

            data type,

            can it be null,

            default value,

            is it a primary key,
        ),]
        """
        command = f'PRAGMA table_info("{table_name}")'
        try:
            self.cur.execute(command)
            return self.cur.fetchall()
        except Exception as e:
            print(e)
            return e

    def execute_cmd(self, cmd):
        try:
            self.cur.execute(cmd)
            self.con.commit()
        except Exception as e:
            print('⭕', e)

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

