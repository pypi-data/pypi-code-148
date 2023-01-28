"""Le module scrippy_mail.mail.PopClient est une implémentation basique du protocole POP3."""
import time
import socket
import logging
from io import BytesIO
from scrippy_mail import ScrippyMailError


class PopClient:
  """L'objet PopClient implémente une partie du protocle POP3 (RFC 1939).

  https://tools.ietf.org/html/rfc1939

  Par défaut le serveur POP3 utilisé est la machine locale '127.0.0.1'.
  """

  def __init__(self, host='127.0.0.1', port=110, timeout=2):
    """Initialise le client."""
    self.host = host
    self.port = port
    self.timeout = timeout
    self.socket = None

  def connect(self):
    """Se connecte sur le serveur distant."""
    logging.info("[+] Connexion au serveur de courriels")
    logging.info(f" '-> {self.host}:{self.port}")
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(self.timeout)
    try:
      self.socket.connect((self.host, self.port))
      self._recv_data()
    except Exception as err:
      err_msg = f"Erreur lors de la connexion: [{err.__class__.__name__}] {err}"
      logging.critical(f" '-> {err_msg}")
      raise ScrippyMailError(err_msg) from err

  def _send_data(self, data):
    """
    Envoie au serveur distant et via le socket les données passées en argument.

    Cette méthode est à usage interne et ne devrait pas etre utilisée directement.
    """
    try:
      self.socket.sendall(data)
      logging.debug(f"Sent: {data}")
    except Exception as err:
      err_msg = f"Erreur lors de la communication avec le serveur de courriels: [{err.__class__.__name__}]: {err}"
      logging.critical(err_msg)
      raise ScrippyMailError(err_msg) from err

  def _recv_data(self, bufsize=8192):
    """
    Reçoit les données envoyées par le serveur distant au travers du socket.

    Cette méthode est à usage interne et ne devrait pas etre utilisée directement.
    """
    data = b''
    start = time.time()
    try:
      while time.time() - start < self.timeout:
        try:
          packet = self.socket.recv(bufsize)
          data += packet
        except Exception as err:
          # On recommence jusqu'à expiration du timeout
          logging.debug(f"{time.time() - start}/{self.timeout}")
          logging.debug(f"{err.__class__.__name__}]: {err}")
      logging.debug(f"Received: {data}")
      return data
    except Exception as err:
      err_msg = f"Erreur lors de la communication avec le serveur de courriels: [{err.__class__.__name__}]: {err}"
      raise ScrippyMailError(err_msg) from err

  def authenticate(self, username, password):
    """
    Authentification de l'utilisateur.

    Lève une erreur ScrippyMailError si l'authentification n'est réussie.
    """
    logging.info("[+] Auhentification")
    logging.debug(f" '-> {username}:{password}")
    buffer = BytesIO()
    buffer.write(b'USER %s\r\n' % username.encode())
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Erreur lors de l'authentification: {resp}"
      logging.critical(f" '-> {err_msg}")
      raise ScrippyMailError(err_msg)
    buffer = BytesIO()
    buffer.write(b'PASS %s\r\n' % password.encode())
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Erreur lors de l'authentification: {resp}"
      raise ScrippyMailError(err_msg)

  def stat(self):
    """
    Récupère le nombre de messages disponibles dans la boite de l'utilisateur.

    Lève une erreur ScrippyMailError si l'authentification échoue.
    """
    logging.info("[+] Recuperation du nombres de courriels disponibles")
    buffer = BytesIO()
    buffer.write(b'STAT\r\n')
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Erreur lors de la recuperation du nombre de courriels: {resp}"
      raise ScrippyMailError(err_msg)
    return resp

  def retr(self, num):
    """
    Récupère le contenu du courriel dont le numéro est passé en argument.

    Lève une erreur ScrippyMailError si l'authentification échoue.
    """
    logging.info("[+] Recuperation du courriel")
    logging.debug(f" '-> No: {num}")
    buffer = BytesIO()
    buffer.write(b'RETR %d\r\n' % num)
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Erreur lors de la recuperation du courriel: {resp}"
      raise ScrippyMailError(err_msg)
    # On ne renvoie que le mail (sans le code de réponse du serveur)
    return resp.split(b'\r\n', 1)[1]

  def dele(self, num):
    """
    Supprime le contenu du courriel dont le numéro est passé en argument.

    Lève une erreur ScrippyMailError si l'authentification échoue.
    """
    logging.info("[+] Suppression du courriel")
    logging.debug(f" '-> No: {num}")
    buffer = BytesIO()
    buffer.write(b'DELE %d\r\n' % num)
    self._send_data(buffer.getvalue())
    resp = self._recv_data()
    if resp[:3] != b'+OK':
      err_msg = f"Erreur lors de la suppression du courriel: {resp}"
      raise ScrippyMailError(err_msg)
    return resp

  def bye(self):
    """Se déconnecte du serveur distant."""
    logging.info("[+] Deconnexion du serveur de courriels")
    buffer = BytesIO()
    buffer.write(b'QUIT\r\n')
    self._send_data(buffer.getvalue())
    self.socket.shutdown(socket.SHUT_WR)
