import sqlite3
import os
from celestis.model import exceptions

class Table:
    def __init__(self, table_name, project_path):
        self.table_name = table_name
        self.db_file = os.path.join(project_path, "db.sqlite3")
    
    def add(self, record):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        # Check if table exists
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (self.table_name,))
        result = c.fetchone()
        
        if result:
            rows = ", ".join("?" for _ in record.values())
            c.execute(f"INSERT INTO {self.table_name} VALUES ({rows})", tuple(record.values()))
        else:
            raise exceptions.TableNotFoundError(self.table_name)
        
        conn.commit()
        conn.close()
    
    def find(self, conditions):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        query = f"SELECT * FROM {self.table_name} WHERE "

        args = []

        for key, value in conditions.items():
            query += f"{key} = ? AND"
            args.append(value)
        
        query = query[:-4]

        c.execute(query, tuple(args))
        result = c.fetchall()

        conn.close()

        # return result [("email.com", "pass")] [{"email": "email.com", "password": "pass"}]
        if len(result) >= 1:
            field_names = [i[0] for i in c.description]
            output = [{field_names[i]: row[i] for i in range(len(field_names))} for row in result]
            
            if len(output) == 1:
                return output[0]
            
            return output
        else:
            return None
        
    def delete(self, record):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        query = f"DELETE FROM {self.table_name} WHERE "

        args = []

        for key, value in record.items():
            query += f"{key} = ? AND "
            args.append(value)
        
        query = query[:-4]
        c.execute(query, tuple(args))

        conn.commit()
        conn.close()
    
    def update(self, record, **kwargs):
        self.delete(record)

        for key, value in kwargs.items():
            if key in record:
                record[key] = value
            else:
                raise exceptions.FieldNotFoundError(key)
        
        self.add(record)
        
users = Table("users", os.getcwd())

# Creating a new record in a table
# users.add({
#     "email": "john@gmail.com",
#     "password": "pass"
# })

# Reading from a table
output = users.find({
    "password": "pass"
})

print(output)

# Update the table
users.update(output, password="pass@123", email="google@gmail.com")
