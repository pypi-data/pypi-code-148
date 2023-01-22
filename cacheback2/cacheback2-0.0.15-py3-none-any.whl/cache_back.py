import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from . import headers
import hashlib

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = 5432  # default
BLOB_TABLE_NAME = "pipeline_blobs"
CACHE_TABLE_NAME = "cached_tables"
NOTEBOOK_NAME = ""
NOTEBOOK_CODE = ""
_cached_objects = {}


def init_session(notebook_name, db_name, db_user, db_pass, db_host, db_port=5432):
    """ Initialises Database parameters for connection to postgres """
    global DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASS = db_pass
    DB_HOST = db_host
    DB_PORT = db_port
    NOTEBOOK_NAME = notebook_name
    print(DB_USER, DB_PASS, DB_HOST, DB_PORT)
    print('init session invoked')


def _connect():
    """ Connect to postgres and retrieve all cached variables back into the script """
    conn = psycopg2.connect(database=DB_NAME,
                            user=DB_USER,
                            password=DB_PASS,
                            host=DB_HOST,
                            port=DB_PORT)
    print('_connect invoked')
    return conn


def insert(df, source_db_name, destination_db_table):
    """ Inserts a given dataframe into postgres """
    try:
        conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{source_db_name}"
        db = create_engine(conn_string)
        conn = db.connect()
        df.to_sql(destination_db_table, con=conn, if_exists='replace', index=False)
        print(f"Cached Dataframe successfully to table: {destination_db_table}")
    except Exception as e:
        print(e.args)


# When executing code,
# 1. get all lists of pandas dataframes
# 2. insert them into cached table (cached_tables)

# the default behaviour of commit should be every pandas table needs to be cached
def execute_as_plpython(notebook_path, function_name):
    """ Takes a jupyter notebook and runs it as a plpython function on Postgres Server """
    try:
        plpython_query = headers.generate_query(notebook_path,
                                                function_name,
                                                add_code_for_caching=True)
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        print(plpython_query)
        print(conn)

        cur = conn.cursor()
        print(cur)
        cur.execute(plpython_query)

        cur.execute(f"SELECT {function_name}();")
    except Exception as e:
        print(e.args)


def add_to_cache(object, name):
    _cached_objects[name] = object
    print(f"Object added to cache. Current Cache: {_cached_objects.keys()}")


def view_cache():
    print(_cached_objects)


def remove_from_cache(object_name):
    if object_name in _cached_objects.keys():
        del _cached_objects[object_name]
        print(f"Removed {object_name}")
    else:
        raise Exception(f"{object_name} not found.")


def cache_tables():
    # if no table is specified for caching, cache everything!
    conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    db = create_engine(conn_string)
    conn = db.connect()
    for i in dir():
        if not i.startswith('__'):
            if type(eval(i)) == pd.DataFrame:
                eval(i).to_sql(i, con=conn, if_exists='replace', index=False)
                print(i, "is being inserted")


def send_blob(id, notebook_path, file_name):
    _create_blob_table()
    try:

        file_data = read_notebook_as_binary(notebook_path)
        blob = psycopg2.Binary(file_data)
        conn = _connect()
        cur = conn.cursor()
        query = f"INSERT INTO {BLOB_TABLE_NAME} (id, file_name, source_notebook, plscript, timestamp) VALUES({id},'{file_name}',{blob},'plpythonscript', NOW())"
        cur.execute(query)
        print('Inserted notebook as blob')
        conn.commit()
        cur.close()
    except Exception as e:
        print(e.args)


def _create_blob_table():
    print('Trying to create blob table')
    try:
        conn = _connect()
        cur = conn.cursor()
        query = f"CREATE TABLE IF NOT EXISTS {BLOB_TABLE_NAME} (id INT, file_name TEXT, source_notebook BYTEA, plscript TEXT, updated_notebook BYTEA, timestamp TIMESTAMP WITH TIME ZONE NOT NULL);"
        cur.execute(query)
        conn.commit()
        cur.close()
    except Exception as e:
        print(e.args)


def read_notebook_as_binary(notebook_path):
    with open(notebook_path, 'rb') as file:
        data = file.read()
    return data


def read_existing_cache(notebook_path: str):
    """
    Attempts to check whether DBMS already has existing cache for current notebook.
    If it does not exist, prints that the cache does not exist.
    """
    print("Attemping to retrieve cache (if existing)")
    try:
        conn = _connect()
        cur = conn.cursor()
        file_data = read_notebook_as_binary(notebook_path)
        blob = psycopg2.Binary(file_data)
        query = f"SELECT * FROM {BLOB_TABLE_NAME} WHERE source_notebook = {blob}"
        cur = conn.cursor()
        cur.execute(query)
        res = cur.fetchall()
        print(res)
        cur.close()

    except Exception as e:
        print(e.args)


def generate_var_name(df_name, filename=NOTEBOOK_NAME):
    hash = hashlib.md5(filename.encode()).hexdigest()
    generated_name = df_name + hash
    return generated_name


def cache_from_list():
    try:
        for df_name, df in _cached_objects.items():
            df_table = generate_var_name(df_name)
            insert(df, source_db_table="reviews_data", destination_db_table=df_table)
            # _cache_outputs[df_name] = f"SELECT * FROM {df_table}"

        # rewrite_pipeline()
    except Exception as e:
        print(e.args[0])