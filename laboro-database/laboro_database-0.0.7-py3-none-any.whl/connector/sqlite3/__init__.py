import logging
import sqlite3

logger = logging.getLogger("laboro.main")


class DbSqlite3:

  @staticmethod
  def connect(username=None,
              password=None,
              host=None,
              port=None,
              database=None,
              service=None):
    return sqlite3.connect(database=database)

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
