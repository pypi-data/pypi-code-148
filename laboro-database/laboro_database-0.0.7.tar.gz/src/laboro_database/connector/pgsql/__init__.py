import logging
import psycopg2

logger = logging.getLogger("laboro.main")


class DbPgsql:

  @staticmethod
  def connect(username=None,
              password=None,
              host=None,
              port=None,
              database=None,
              service=None):
    if service is not None:
      return psycopg2.connect(service=service)
    return psycopg2.connect(user=username,
                            host=host,
                            port=port,
                            dbname=database,
                            password=password)

  @staticmethod
  def query(cursor, request, params=None, verbose=False):
    if verbose:
      logger.info(f"Request: {request}")
      logger.info(f"Params: {params}")
    if params is not None:
      cursor.execute(request, params)
    else:
      cursor.execute(request)
    try:
      rows = cursor.fetchall()
      if verbose:
        for row in rows:
          logger.info(f"{' | '.join([str(i) for i in row])}")
      return rows
    except psycopg2.ProgrammingError:
      return list()
