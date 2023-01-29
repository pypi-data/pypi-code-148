import logging
import socket
import ssl
from laboro_ftp.clients.errors import Error
from laboro_ftp.clients.ftps import Ftps

logger = logging.getLogger("laboro.main")


class Ftpes(Ftps):
  """
  Ftp client with explicit TLS support (FTPes).
  """

  ssl_version = None
  ssl_verify = True
  ssl_session = None
  context = None
  _prot_p = False

  def __init__(self, hostname, port=21,
               username='anonymous', password='anonymous',
               ssl_verify=True, ssl_version=None):
    super().__init__(hostname=hostname, port=port,
                     username=username, password=password)
    self.ssl_verify = ssl_verify
    self.ssl_version = ssl.PROTOCOL_TLS_CLIENT
    if ssl_version is not None:
      self.ssl_version = getattr(ssl.TLSVersion, ssl_version)
    self.context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    if not self.ssl_verify:
      self.context.check_hostname = False
      self.context.verify_mode = ssl.CERT_NONE

  def connect(self):
    logger.debug("[+] Connection (Explicit TLS)")
    if self.hostname is not None:
      self.sock = socket.create_connection((self.hostname, self.port),
                                           self.timeout)
      self.af = self.sock.family
      if not self.ssl_verify:
        logger.warning("[!] Insecure connection: ssl_verify set to False")
      self.file = self.sock.makefile('r', encoding=self.ENCODING)
      logger.debug(f"[WELCOME] {self._getresp()}")
      self.auth()
      logger.debug("[=] connected")
      return True
    raise Error("Remote host not defined")

  def auth(self):
    if isinstance(self.sock, ssl.SSLSocket):
      raise ValueError("Connection is already secured")
    if self.ssl_version >= ssl.PROTOCOL_TLS:
      resp = self.voidcmd('AUTH TLS')
    else:
      resp = self.voidcmd('AUTH SSL')
    self.sock = self.context.wrap_socket(self.sock,
                                         server_hostname=self.hostname)
    self.file = self.sock.makefile(mode='r', encoding=self.ENCODING)
    return resp
