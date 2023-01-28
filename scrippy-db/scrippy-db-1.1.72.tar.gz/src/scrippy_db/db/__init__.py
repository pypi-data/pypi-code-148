import logging
import psycopg2
import cx_Oracle
from scrippy_db import ScrippyDbError


class Db:
  """Classe générique pour le client de base de données."""

  def __init__(self, username=None, host=None, database=None, port=None, password=None, service=None, db_type="postgres"):
    """Initialise le client."""
    self.db_types = {"postgres": {"connect": self.connect_pgsql,
                                  "execute": self.execute_pgsql},
                     "oracle": {"connect": self.connect_oracle,
                                "execute": self.execute_oracle}}
    self.username = username
    self.host = host
    self.database = database
    self.port = port
    self.password = password
    self.service = service
    self.db_type = db_type
    self.connection = None
    self.cursor = None

  def __enter__(self):
    """Point d'entrée."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Point de sortie."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """Se connecte à la base.

    Méthode générique.
    """
    try:
      logging.info("[+] Connexion au service de base de donnees:")
      self.connection = self.db_types[self.db_type]["connect"]()
    except (psycopg2.Error, cx_Oracle.DatabaseError) as err:
      err_msg = f"Erreur lors de la connexion: [{err.__class__.__name__}] {err}"
      raise ScrippyDbError(err_msg) from err

  def connect_oracle(self):
    """Se connecte à la base Oracle."""
    dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.database)
    logging.info(f" '-> {dsn}")
    return cx_Oracle.connect(self.username, self.password, dsn)

  def connect_pgsql(self):
    """Se connecte à la base Postgres."""
    if self.service:
      logging.info(f" '-> {self.service}")
      return psycopg2.connect(service=self.service)
    logging.info(f" '-> {self.username}@{self.host}:{self.port}/{self.database}")
    return psycopg2.connect(user=self.username,
                            host=self.host,
                            port=self.port,
                            dbname=self.database,
                            password=self.password)

  def close(self):
    """Ferme la connexion."""
    try:
      if self.cursor:
        self.cursor.close()
    except (psycopg2.Error, cx_Oracle.InterfaceError) as err:
      logging.warning(f" '-> Erreur lors de la fermeture de la connexion: [{err.__class__.__name__}] {err}")
    finally:
      if self.connection:
        logging.info("[+] Fermeture de la connexion a la base de donnees")
        self.connection.close()
        self.connection = None

  def execute(self, request, params=None, verbose=False, commit=False):
    """Exécute la requète SQL.

    Méthode générique.
    """
    try:
      logging.info("[+] Exécution de la requète:")
      result = self.db_types[self.db_type]["execute"](request,
                                                      params,
                                                      verbose)
      if commit:
        self.connection.commit()
      return result
    except Exception as err:
      logging.error(f" '-> Erreur lors de l'execution de la requete [{err.__class__.__name__}] {err}")
      self.connection.rollback()
      self.close()

  def execute_oracle(self, request, params, verbose):
    """Exécute la requète SQL (Oracle)."""
    with self.connection.cursor() as self.cursor:
      if verbose:
        logging.info(f" '-> {request}")
        logging.info(f" '-> {params}")
      if params is not None:
        self.cursor.execute(request, params)
      else:
        self.cursor.execute(request)
      logging.debug(f" '-> {self.cursor.rowcount} ligne(s) impactee(s)")
      try:
        result = self.cursor.fetchall()
      except cx_Oracle.InterfaceError:
        logging.debug(" '-> Aucun resultat a recuperer")
        return None
      if verbose:
        for row in result:
          logging.info(f"  '-> {' | '.join([str(i) for i in row])}")
      return result

  def execute_pgsql(self, request, params, verbose):
    """Exécute la requète SQL (Postgres)."""
    with self.connection.cursor() as self.cursor:
      if verbose:
        logging.info(f" '-> {self.cursor.mogrify(request, params)}")
      self.cursor.execute(request, params)
      logging.debug(f" '-> {self.cursor.rowcount} ligne(s) impactee(s)")
      try:
        result = self.cursor.fetchall()
      except psycopg2.ProgrammingError:
        logging.debug(" '-> Aucun resultat a recuperer")
        return None
      if verbose:
        for row in result:
          logging.info(f"  '-> {' | '.join([str(i) for i in row])}".format())
      return result


class ConnectionChain:
  """L'objet ConnectionChain permet de retrouver les informations de connexions
     à une base de données à partir d'une chaîne de caractères répondant au
     format <DB_TYPE>:<ROLE>/<PASSWORD>@<HOST>:<PORT>//<DB_NAME>."""

  def __init__(self, connection_chain):
    """Initialise la chaîne de connexion."""
    self.db_type = connection_chain.split(':')[0]
    self.username = connection_chain.split(':')[1].split('/')[0]
    self.password = connection_chain.split('@')[0].split('/')[1]
    self.host = connection_chain.split('@')[1].split(':')[0]
    self.port = int(connection_chain.split(':')[2].split('/')[0])
    self.database = connection_chain.split('/')[-1]


class DbFromCc(Db):
  """Classe spécifique permettant l'instanciation d'un objet Db à l'aide d'un objet ConnectionChain."""

  def __init__(self, connection_chain):
    """Initialise un client de BDD à partir de la chaîne de connexion."""
    c_chain = ConnectionChain(connection_chain)
    super().__init__(username=c_chain.username,
                     host=c_chain.host,
                     database=c_chain.database,
                     port=c_chain.port,
                     password=c_chain.password,
                     service=None,
                     db_type=c_chain.db_type)
