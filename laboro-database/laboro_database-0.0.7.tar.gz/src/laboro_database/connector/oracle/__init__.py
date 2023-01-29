import logging
import cx_Oracle

logger = logging.getLogger("laboro.main")


class DbOracle:

  @staticmethod
  def connect(username=None,
              password=None,
              host=None,
              port=None,
              database=None,
              service=None):
    dsn = cx_Oracle.makedsn(host, port, service_name=database)
    return cx_Oracle.connect(username, password, dsn)

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
    except cx_Oracle.InterfaceError:
      return list()
