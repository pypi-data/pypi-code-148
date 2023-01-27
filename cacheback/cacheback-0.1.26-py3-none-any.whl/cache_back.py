import psycopg2
from sqlalchemy import create_engine
import pandas as pd
from . import headers
import hashlib
from . import dependency as dep

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = 5432 # default
BLOB_TABLE_NAME = "pipeline_blobs"
NOTEBOOK_NAME = ""
NOTEBOOK_CODE = ""
cached_objects = {}
cache_outputs = {}
cache_namespaces = {}
CACHE_TABLE_NAME = "cached_tables"

def init_session(db_name, db_user, db_pass, db_host, db_port=5432, notebook_name=''):
    """ Initialises Database parameters for connection to postgres """
    global DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT, NOTEBOOK_CODE, NOTEBOOK_NAME
    DB_NAME = db_name
    DB_USER = db_user
    DB_PASS = db_pass
    DB_HOST = db_host
    DB_PORT = db_port
    NOTEBOOK_NAME = notebook_name
    # dep.handle_imports(notebook_name + '.ipynb')
    print(DB_USER,DB_PASS, DB_HOST, DB_PORT)
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


def insert(df, destination_db_table):
    """ Inserts a given dataframe into postgres """
    try:
        conn_string = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        db = create_engine(conn_string)
        conn = db.connect()
        df.to_sql(destination_db_table, con=conn, if_exists='replace', index=False)
        print(f"Cached Dataframe successfully to table: {destination_db_table}")
    except Exception as e:
        print(e.args[0])


# When executing code,
# 1. get all lists of pandas dataframes
# 2. insert them into cached table (cached_tables)

# the default behaviour of commit shouldstart_time be every pandas table needs to be cached
def execute_as_plpython(notebook_path, function_name):
    """ Takes a jupyter notebook and runs it as a plpython function on Postgres Server """
    try:
        plpython_query = headers.generate_query(notebook_path,
                                                function_name,
                                                add_code_for_caching=False,
                                                is_query=False)

        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

        print(f"EXECUTING -->\n{plpython_query}")
        cur = conn.cursor()
        cur.execute(plpython_query)

        print('RUNNING SCRIPT')
        cur.execute(f"SELECT {function_name}();")
        print('Successful execution of plpython')
        conn.commit()
        cur.close()

    except Exception as e:
        print(e.args[0])

def add_to_cache(object, name=''):
    if name == '':
        name = 'cache_object_' + str(len(cached_objects))
    cached_objects[name] =  object
    cache_namespaces[name] = get_var_local_name(object)
    print(f"Object added to cache. Current Cache: {cached_objects.keys()}")

def view_cache():
    print(cached_objects)

def remove_from_cache(object_name):
    if object_name in cached_objects.keys():
        del cached_objects[object_name]
        print(f"Removed {object_name}")
    else:
        raise Exception(f"{object_name} not found.")


def send_blob(notebook_path, file_name):
    _create_blob_table()
    try:
        conn = _connect()
        cur = conn.cursor()
        file_data = read_notebook_as_binary(notebook_path)
        
        function_name = headers.get_notebook_name(notebook_path) + '_script'

        plpython_script = headers.generate_query(notebook_path, function_name, is_query=True)
        print('generated query')
        blob = psycopg2.Binary(file_data)

        print('file read as binary')

        query = f"INSERT INTO {BLOB_TABLE_NAME} (file_name, source_notebook, plscript) VALUES('{file_name}',{blob},'''{plpython_script}''')"

        cur.execute(query)
        print('Blob inserted')
        conn.commit()
        cur.close()

        execute_as_plpython(notebook_path, 'execute_plpython')
        print_debugs()
        
    except Exception as e:
        print(e.args[0])

def _create_blob_table():
    try:
        conn = _connect()
        cur = conn.cursor()
        query = f"CREATE TABLE IF NOT EXISTS {BLOB_TABLE_NAME} (id SERIAL PRIMARY KEY, upload_date TIMESTAMP default current_timestamp, file_name TEXT, source_notebook BYTEA, plscript TEXT, updated_notebook BYTEA);"
        print(query)

        cur.execute(query)
        conn.commit() 
        cur.close()
    except Exception as e:
        print(e.args)

def read_notebook_as_binary(notebook_path):
    with open(notebook_path, 'rb') as file:
        data = file.read()
    return data

def cache_from_list():
    global NOTEBOOK_CODE 
    NOTEBOOK_CODE = fetch_notebook_code()
    print('caching from list ... ')
    try:
        print('Caching Objects ... ')

        for df_name, df in cached_objects.items():
            print(f"inserting {df_name} ...")
            df_table = generate_var_name(df_name)
            insert(df,destination_db_table=df_table)
            cache_outputs[df_name] = f"SELECT * FROM {df_table}"
            NOTEBOOK_CODE = headers.comment_line_by_var_usage(df_name, NOTEBOOK_CODE)
        
        print(f"Cache outputs : {cache_outputs}")
        
        NOTEBOOK_CODE = rewrite_pipeline(NOTEBOOK_CODE)
    except Exception as e:
        print(e.args[0])

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
    generated_name = df_name + '_' + hash
    return generated_name

def rewrite_pipeline(notebook_code):
    print(f"before : NOTEBOOK CODE = {notebook_code}")
    l0 = "import psycopg2"
    l1 = f"conn = psycopg2.connect(database='{DB_NAME}', user='{DB_USER}', password='{DB_PASS}', host='{DB_HOST}', port='{DB_PORT}')"
    l2 = "cur = conn.cursor()"
    query_code = ''
    for df_name, query in cache_outputs.items():
        notebook_code = headers.comment_line_by_var_usage(df_name, notebook_code)
        query_code = query_code + get_sql_conn_code(query=query, df_name=df_name)
    
    notebook_code = notebook_code + l1 + '\n' + l2 + '\n' + query_code + '\n'
    return notebook_code

def get_sql_conn_code(query, df_name):
    l3 = f"cur.execute('{query}')"
    l4 = f"res_{df_name} = cur.fetchall()"
    l5 = f"{df_name} = pd.DataFrame(res_{df_name})"
    return l3 + '\n' + l4 + '\n'+ l5 + '\n' 

def get_updated_notebook():
    return NOTEBOOK_CODE

def print_debugs():
    global NOTEBOOK_CODE
    try:
        print(f"Cached obj: {cached_objects}")
        print(f"Cached obj: {cache_outputs}")
        print(f"Cached namespaces: {cache_namespaces}")
        print(f"Notebook code: {NOTEBOOK_CODE}")
    except Exception as e:
        print(e.args)

def fetch_notebook_code():
    try:
        print('fetching notebook..')
        conn = _connect()
        cur = conn.cursor()
        query = f"SELECT source_notebook FROM {BLOB_TABLE_NAME} WHERE upload_date=(SELECT MAX(upload_date) FROM {BLOB_TABLE_NAME})"
        cur.execute(query)
        binary_notebook = cur.fetchall()[0]
        notebook_str = ''
        for bytes in binary_notebook[0]:
            notebook_str = notebook_str + bytes.decode("utf-8") 
        print('notebook fetched')

        return headers.get_code_from_json(notebook_str)
        
    except Exception as e:
        print(e.args)


def get_var_local_name(data_obj):
    for x in globals():
        if globals()[x] is data_obj:
            return x

def fetch_updated_code():
    try:
        conn = _connect()
        cur = conn.cursor()
        query = f"SELECT updated_notebook FROM {BLOB_TABLE_NAME} WHERE upload_date=(SELECT MAX(upload_date) FROM {BLOB_TABLE_NAME})"
        cur.execute(query)
        binary_notebook = cur.fetchall()[0]
        notebook_str = ''
        for bytes in binary_notebook[0]:
            notebook_str = notebook_str + bytes.decode("utf-8") 

        return notebook_str
        
    except Exception as e:
        print(e.args)

def export_notebook(directory):
    """ Exports the latest notebook, assumes that latest notebook has already over-written updated_notebook field """
    notebook_code = fetch_updated_code()
    filename = directory  + '/' + NOTEBOOK_NAME + '_updated_pipeline.ipynb'
    f = open(filename, "w")
    f.write(notebook_code)
    f.close()
    print(f'Updated Notebook downloaded to {filename} successfully')
    
def update_pipeline():
    try:
        conn = _connect()
        cur = conn.cursor()
        # query = f"INSERT INTO {BLOB_TABLE_NAME} (updated_noteebook) VALUES('{file_name}',{blob},'''{plpython_script}''')"

        query = f"SELECT updated_notebook FROM {BLOB_TABLE_NAME} WHERE upload_date=(SELECT MAX(upload_date) FROM {BLOB_TABLE_NAME})"
        cur.execute(query)
        binary_notebook = cur.fetchall()[0]
        notebook_str = ''
        for bytes in binary_notebook[0]:
            notebook_str = notebook_str + bytes.decode("utf-8") 

    except Exception as e:
        print(e.args)