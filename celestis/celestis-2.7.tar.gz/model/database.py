import os
import sqlite3
import re
import importlib.util

def extract_table_information(tables_file):
    with open(tables_file, "r") as f:
        contents = f.read()
    
    
    table_names = re.findall(r"def (\w+)\(", contents)
    # [users, posts, ...]

    spec = importlib.util.spec_from_file_location("tables", str(tables_file))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    tables = []

    for item in table_names:
        fields = getattr(module, item)()

        table_info = {
            "table": item,
            "fields": fields
        }

        tables.append(table_info)
    
    return tables


def read_db(project_path):
    tables_file = os.path.join(project_path, "tables.py")
    db_file = os.path.join(project_path, "db.sqlite3")

    if os.path.exists(tables_file):
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        tables_info = extract_table_information(tables_file)
        print(tables_info)
        for item in tables_info:
            table_name = item["table"]
            table_fields = item["fields"]

            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = c.fetchone()

            field_str = ', '.join(f"{key} {value}" for key, value in table_fields.items())
            # {"email": "TEXT PRIMARY KEY", "password": "TEXT"} -> 'email TEXT PRIMARY KEY, password: TEXT'
            if not result:
                c.execute(f"CREATE TABLE {table_name} ({field_str})")
            else:
                print(f"Table {table_name} already exist, skipping creation")
            
        conn.commit()
        conn.close()
