# from preql.compiler import compile
from os.path import dirname, join

from sqlalchemy.engine import create_engine, url

from preql import Executor, Dialects
from preql.dialect.sql_server import SqlServerDialect
from preql.parser import parse
from urllib.parse import quote_plus


WORKING_STRING = r'Trusted_Connection=YES;TrustServerCertificate=YES;DRIVER={ODBC Driver 18 for SQL Server};SERVER=LAPTOP-BIINRSI2\SQLEXPRESS'

params = quote_plus(WORKING_STRING)

#engine = sqlalchemy.create_engine('mssql://*server_name*\\SQLEXPRESS/*database_name*?trusted_connection=yes')
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
# validate connection
engine.engine.execute('select 1').fetchall()

with open(join(dirname(__file__), 'three_part_join_debug.preql'), 'r', encoding='utf-8') as f:
    file = f.read()

environment, statements = parse(file)

generator = SqlServerDialect()

executor = Executor(dialect=Dialects.SQL_SERVER, engine=engine)

sql = generator.generate_queries(environment, statements)

for statement in sql:
    sql = generator.compile_statement(statement)
    print(sql)
    results = executor.execute_query(statement)
    for row in results:
        print(row)
