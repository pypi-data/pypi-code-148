import logging
from laboro.error import LaboroError
from laboro.module import Module
from laboro_database.connector.pgsql import DbPgsql
from laboro_database.connector.sqlite3 import DbSqlite3
from laboro_database.connector.mysql import DbMysql


class Database(Module):
  """This module is derivated from the ``laboro.module.Module`` base class.

  Its purpose is to provide a simplified interface to all major relational database types.

  Arguments:
    args: A dictionary specifying the database connection parameters and database type. Most of the arguments are optional depending of the database type.

      ``username``: String. Optional.
      ``password``: String. Optional.
      ``host``: String. Optional.
      ``port``: Int. Optional.
      ``service``: String. A PostgresSQL service name. Optional.
      ``database``: The database name. Mandatory.
      ``db_type``: String, one of `postgres`, `sqlite3`, `mysql`. Mandatory.

  """

  def __init__(self, context, args=None):
    super().__init__(filepath=__file__, context=context, args=args)
    self.connectors = {"pgsql": DbPgsql,
                       "sqlite3": DbSqlite3,
                       "mysql": DbMysql}
    self.connector = None
    self.connection = None
    self.cursor = None

  def __enter__(self):
    super().__enter__()
    self.connector = self.connectors[self.args.get("db_type")]
    return self

  def __exit__(self, kind, value, traceback):
    if self.connection is not None:
      self.connection.close()

  def connect(self):
    """
    Connects to the database with database connection parameters provided at init time.
    """
    self.context.log.info("Connecting to database...")
    return self.connector.connect(username=self.args.get("username"),
                                  password=self.args.get("password"),
                                  host=self.args.get("host"),
                                  port=self.args.get("port"),
                                  database=self.args.get("database"),
                                  service=self.args.get("service"))

  @Module.laboro_method
  def query(self, request, params=None, commit=False,
            verbose=False, exit_on_error=True):
    """Prepare and execute the specified query on the database.
    In conformance to `Python Database API v2.0` (See https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while request execution, the request will be `rollbacked`.

    Arguments:
      ``request``: String. The SQL request to execute. The string request should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle)v for parameters mapping.
      ``params``: An optional dictionary specifying the needed parameters to be mapped on the ``request`` string.
      ``commit``: Boolean. When set to `True`, a commit statement will be sent to the database immediately after the request execution.
      ``verbose``: Boolean. If set to `True`, request, parameters and result will be sent to the logger. Default to ``False``
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while request execution will raise an error and exit the workflow after query rollback. Default to ``True``.

    Returns:
      A database ``cursor`` containing the returned values.
    """
    with self.connect() as self.connection:
      self.context.log.info("Querying the database...")
      self.cursor = self.connection.cursor()
      try:
        rows = self.connector.query(cursor=self.cursor,
                                    request=request,
                                    params=params,
                                    verbose=verbose)
        if commit:
          self.connection.commit()
        if len(rows) > 0:
          return rows
        return None
      except Exception as err:
        self.context.log.error(f"[{err.__class__.__name__}] {err}")
        self.context.log.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise LaboroError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err

  @Module.laboro_method
  def multi_query(self, request, paramlist, commit=False,
                  verbose=False, exit_on_error=False):
    """Prepare and execute the specified query on the database for each set of parameters found in the`` paramlist`` argument.
    In conformance to `Python Database API v2.0` (See https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while request execution, the request will be `rollbacked`.

    This method is intended to insert data or update the database. It is not intended to retrieve data.

    Arguments:
      ``request``: String. The SQL request to execute. The string request should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle) for parameters mapping.
      ``paramlist``: An mandatory list of dictionaries specifying the needed parameters to be mapped on each execution of the ``request`` string.
      ``commit``: Boolean. When set to `True`, a commit statement will be sent to the database immediately after each request execution.
      ``verbose``: Boolean. If set to `True`, each request, parameters and result will be sent to the logger.
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while one of the request executions will raise an error and exit the workflow after current query rollback.

    Returns: None"""
    self.context.log.info("Querying the database...")
    with self.connect() as self.connection:
      self.cursor = self.connection.cursor()
      try:
        for params in paramlist:
          rows = self.connector.query(cursor=self.cursor,
                                      request=request,
                                      params=params,
                                      verbose=verbose)
          if commit:
            self.connection.commit()
      except Exception as err:
        self.context.log.error(f"[{err.__class__.__name__}] {err}")
        self.context.log.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise LaboroError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err

  @Module.laboro_method
  def transaction(self, requests, verbose=False, exit_on_error=False):
    """Prepare and execute on the database as a single transaction each request found in the ``requests`` list.

    The whole transaction is committed only if all queries specified in the ``requests`` argument are executed without error. If an error occurs within the transaction, the whole transaction is rollbacked.

    This method is intended to insert data or update the database. It is not intended to retrieve data.

    Arguments:
      ``requests``: A list of dictionaries specifying all requests and needed parameters to be executed within the transaction. The SQL request to execute. The string request should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle) for parameters mapping.

      Each dictionary in the ``requests`` list must provide at least a ``query`` item specifying a request to execute. It may also provide a ``params`` item which is a dictionary of parameters to be mapped onto the ``query`` string (see the ``query()`` method for further details).
      ``verbose``: Boolean. If set to `True`, each request, parameters and result will be sent to the logger.
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while one of the request executions will raise an error and exit the workflow after transaction rollback

    Returns: None"""

    self.context.log.info("Beginning transaction...")
    with self.connect() as self.connection:
      self.cursor = self.connection.cursor()
      try:
        for request in requests:
          rows = self.connector.query(cursor=self.cursor,
                                      request=request.get("query"),
                                      params=request.get("params"),
                                      verbose=verbose)
        self.connection.commit()
      except Exception as err:
        self.context.log.error(f"[{err.__class__.__name__}] {err}")
        self.context.log.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise LaboroError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err
