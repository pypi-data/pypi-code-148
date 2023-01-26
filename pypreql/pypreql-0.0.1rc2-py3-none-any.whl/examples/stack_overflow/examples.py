from os.path import dirname, join
from logging import StreamHandler, getLogger, DEBUG

logger=getLogger('preql')
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

from sqlalchemy.engine import create_engine
from preql.dialect.bigquery import BigqueryDialect
from preql import Executor, Dialects
from preql.parser import parse
from preql.core.query_processor import process_query
engine = create_engine('bigquery://ttl-test-355422/test_tables')

executor = Executor(dialect=Dialects.BIGQUERY, engine=engine)

with open(join(dirname(__file__), 'single_test_query.preql'), 'r', encoding='utf-8') as f:
    file = f.read()

environment, statements = parse(file)

for statement in statements:
    process_query(environment, statement)

generator = BigqueryDialect()

sql = generator.generate_queries(environment, statements)

for statement in sql:
    sql = generator.compile_statement(statement)
    print(sql)
    results = executor.execute_query(statement)
    for row in results:
        print(row)
