import logging
import mysql.connector

logger = logging.getLogger("laboro.main")


class DbMysql:

  @staticmethod
  def connect(username=None,
              password=None,
              host=None,
              port=None,
              database=None,
              service=None):
    return mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   port=port,
                                   database=database)

  @staticmethod
  def query(cursor, request, params=None, verbose=False):
    if verbose:
      logger.info(f"Request: {request}")
      logger.info(f"Params: {params}")
    if params is not None:
      cursor.execute(request, params)
    else:
      cursor.execute(request)
    rows = cursor.fetchall()
    if verbose:
      for row in rows:
        logger.info(f"{' | '.join([str(i) for i in row])}")
    return rows
