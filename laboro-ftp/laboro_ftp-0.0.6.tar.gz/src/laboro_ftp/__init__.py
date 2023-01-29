import os
import re
from laboro.error import LaboroError
from laboro.module import Module
from laboro_ftp.clients.ftp import FtpSimple
from laboro_ftp.clients.ftps import Ftps
from laboro_ftp.clients.ftpes import Ftpes


class Ftp(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a FTP client able to support all type of operations with or without implicit or explicit TLS support.

  Arguments:

    args: A dictionary specifying the FTP connection parameters and client type.

      ``username``: String. Optional, default to 'anonymous'.
      ``password``: String. Optional, default to 'anonymous'.
      ``host``: String. The remote host to connect to.
      ``port``: Int. Optional. The TCP remote port to connect to. Default: ``21``.
      ``tls``: Boolean. Optional, default to True. If set to False, the FTP connection will not be encrypted.
      ``explicit``: Boolean. Optional, When set to True (default), the FTP connection will use explicit TLS (FTPes). If set to False, the connection will use implicit TLS (FTPs).
      ``ssl_verify``: Boolean. Optional. Default to True. If set to False, remote server SSL certificate will not be verified.
      ``ssl_version``: String. Optional. A string specifying the TLS version to use (Usually one of ``TLSv1_3`` or ``TLSv1_2``). Default to auto negotiation between client and server for highest possible security.
  """
  @property
  def connected(self):
    return self.client is not None and self._connected

  def __init__(self, context, args=None):
    super().__init__(filepath=__file__, context=context, args=args)
    self.client = None
    self._connected = False

  def __enter__(self):
    super().__enter__()
    if self.args.get("tls"):
      if self.args.get("explicit"):
        self.client = Ftpes(self.args.get("host"),
                            self.args.get("port"),
                            self.args.get("username"),
                            self.args.get("password"),
                            self.args.get("ssl_verify"),
                            self.args.get("ssl_version"))
      else:
        self.client = Ftps(self.args.get("host"),
                           self.args.get("port"),
                           self.args.get("username"),
                           self.args.get("password"),
                           self.args.get("ssl_verify"),
                           self.args.get("ssl_version"))
    else:
      self.client = FtpSimple(self.args.get("host"),
                              self.args.get("port"),
                              self.args.get("username"),
                              self.args.get("password"))
    return self

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    """Connect to the remote server using the specified connection information.
    """
    self.context.log.info(f"Connecting to {self.args.get('host')}:{self.args.get('port')}")
    self._connected = self.client.connect()
    if self.connected:
      self.client.login()

  def _close(self):
    """Close the connection to remote server.
    """
    if self.connected:
      self.context.log.info(f"Closing connection to {self.args.get('host')}:{self.args.get('port')}")
      if self.client is not None:
        self.client.quit()
        self._connected = False

  @Module.laboro_method
  def get_file(self, remote_file, local_dir,
               create_dirs=False, exit_on_error=True):
    """
    Get file from remote server ``remote_file`` and store it to ``local_dir``.
    If ``create_dir`` is set to ``True``, a directory structure matching the remote directory hierarchy will be created locally.

    Arguments:
      ``remote_file``: The remote filepath to get the file from.
      ``local_dir``: The local directory where to store the local copy of the file.
      ``create_dirs``: Boolean. Optional. Create an exact copy of the remote directory structure. Default: ``False``
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    local_fname = os.path.join(local_dir, os.path.basename(remote_file))
    if create_dirs:
      local_fname = os.path.join(local_dir, remote_file.lstrip("/"))
      self._create_local_dirs(remote_file, local_dir)
    self.context.log.info(f"Getting remote file: {remote_file} => {local_fname} ")
    try:
      self.client.retrbinary(f"RETR {remote_file}",
                             open(local_fname, 'wb').write)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        self.context.log.critical(err_msg)
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  @Module.laboro_method
  def put_file(self, local_file, remote_dir="/",
               create_dirs=False, exit_on_error=True):
    """
    Send local file ``local_file`` to remote directory ``remote_dir``.
    If ``create_dirs`` is set to ``True``, a directory structure matching the local directory hierarchy will be created on the remote host.

    Arguments:
      ``local_file``: String. Local filename full path.
      ``remote_dir``: String. Optional. Remote directory where to store the file. Default to the remote root directory.
      ``create_dirs``: Boolean. Optional. Create all missing directory components found in ``remote_dir``. Default: ``False``.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    remote_dir = remote_dir.lstrip("/")
    remote_file = os.path.basename(local_file)
    remote_fname = os.path.join(remote_dir, remote_file)
    if create_dirs:
      self._create_remote_dirs(remote_dir=remote_dir,
                               exit_on_error=exit_on_error)
      remote_fname = os.path.join(remote_dir, remote_file)
    self.context.log.info(f"Sending file to: {remote_fname}")
    try:
      self.client.storbinary(f"STOR {remote_fname}", open(local_file, "rb"))
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        self.context.log.critical(err_msg)
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

# -----------------------------------------------------------------------------
# Local operations
# -----------------------------------------------------------------------------
  @Module.laboro_method
  def list_local_dir(self, local_dir, file_type="f", pattern=".*"):
    """
    Get the complete list of files or dirs found in the specified local directory and matching the specified file type (f or d) and the specified regular expression pattern.

    Note:
      - This method is **NOT** recursive.
      - The workflow main workspace directory and workflow session workspace directory component of path will be automatically stripped out from

    Arguments:
      ``local_dir``: String. The full path of the local directory to explore. This option is mandatory and has no default value.
      ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
      pattern: String. A regular expression to filter returned values. Default to ``.*``
    """
    dirs = list()
    files = list()
    reg = re.compile(pattern)
    self.context.log.info(f"Exploring {local_dir}")
    try:
      for l_file in os.listdir(local_dir):
        l_full_fname = os.path.join(local_dir, l_file)
        if os.path.isdir(l_full_fname) and re.match(reg, l_full_fname):
          dirs.append(l_full_fname)
        elif os.path.isfile(l_full_fname) and re.match(reg, l_full_fname):
          files.append(l_full_fname)
      if file_type == "f":
        return files
      elif file_type == "d":
        return dirs
    except Exception as err:
      err_msg = f"[FtpLocalError] {err.__class__.__name__} {err}"
      self.context.log.critical(err_msg)
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def local_mirror(self, remote_dir, local_dir, exit_on_error=True):
    """Make a local copy of a remote directory recursively.

    Arguments:
      ``remote_dir``: String. The remote directory full path.
      ``local_dir``: String. The local directory full path.
      ``skip``: Int. Number of path subdirectory to skip. Default to ``0``.
      ``exit_on_error``: Boolean. When set to ``False``, transfer errors are ignored. If set to ``True``, raise error at first transfer error. Default to ``True``.
    """
    if not self.connected:
      self._connect()
    for r_file in self.list_remote_dir(remote_dir=remote_dir,
                                       file_type="f", pattern=".*"):
      self.get_file(remote_file=r_file,
                    local_dir=local_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for r_dir in self.list_remote_dir(remote_dir=remote_dir,
                                      file_type="d", pattern=".*"):
      self.local_mirror(remote_dir=r_dir,
                        local_dir=local_dir,
                        exit_on_error=exit_on_error)

  @Module.laboro_method
  def delete_local_file(self, local_file, exit_on_error=True):
    """
    Delete specified file from local host.

    Arguments:
      ``local_file``: The local filepath to delete.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    self.context.log.info(f"Removing local file: {local_file}")
    try:
      os.remove(local_file)
    except Exception as err:
      err_msg = f"[FtpLocalOSError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  @Module.laboro_method
  def delete_local_dir(self, local_dir, recursive=False, exit_on_error=True):
    """
    Delete specified directory on the local host and its content.
    Whatever the value of the ``recursive``argument, all files within the specified directory will be deleted.
    When ``recursive`` is set to ``True``, all sub directories and their content are deleted.

    Arguments:
      ``local_dir``: The directory to delete.
      ``recursive``: If set to ``True``, delete directory and all its content.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    self.context.log.info(f"Removing local dir: {local_dir}")

    try:
      if recursive:
        for l_dir in self.list_local_dir(local_dir=local_dir, file_type="d"):
          self.delete_local_dir(local_dir=l_dir,
                                recursive=recursive,
                                exit_on_error=exit_on_error)
      for l_file in self.list_local_dir(local_dir=local_dir):
        self.delete_local_file(local_file=l_file, exit_on_error=exit_on_error)
      os.rmdir(local_dir)
    except Exception as err:
      err_msg = f"[FtpLocalOSError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  def _create_local_dirs(self, remote_file, local_dir):
    """
    Create a copy of the remote directory structure for a remote file path.

    Arguments:
      ``remote_file``: String. A remote file path.
      ``local_dir``: String. The local directory within duplicate the remote directory tree.
    """
    hierarchy = os.path.join(*remote_file.split("/")[:-1])
    hierarchy = os.path.join(local_dir, hierarchy)
    self.context.log.info(f"Creating local dir: {hierarchy}")
    try:
      os.makedirs(hierarchy, exist_ok=True)
    except Exception as err:
      err_msg = f"[FtpOSError] {err.__class__.__name__} {err}"
      self.context.log.error(err_msg)
      raise LaboroError(err_msg) from err

# -----------------------------------------------------------------------------
# Remote operations
# -----------------------------------------------------------------------------
  @Module.laboro_method
  def list_remote_dir(self, remote_dir="/", file_type="f", pattern=".*"):
    """
    Get the complete list of files or dirs found in the specified remote directory and matching the specified file type (f or d) and the specified regular expression pattern.

    Note: This method is **NOT** recursive.

    Arguments:
      ``remote_dir``: String. Optional. The full path of the remote directory to explore. Default to remote root dir.
      ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
      pattern: String. A regular expression to filter returned values. Default to ``.*``
    """
    if not self.connected:
      self._connect()
    content = list()
    self.context.log.info(f"Exploring {remote_dir}")
    try:
      self.client.retrlines(f"LIST {remote_dir}", content.append)
      if file_type == 'f':
        reg = re.compile("^-.*")
      elif file_type == 'd':
        reg = re.compile("^d.*")
      content = [os.path.join(remote_dir, f.split()[-1]) for f in content if re.match(reg, f)]
      reg = re.compile(pattern)
      return [f.split()[-1] for f in content if re.match(reg, f)]
    except Exception as err:
      err_msg = f"[FtpRemoteError] {err.__class__.__name__} {err}"
      self.context.log.critical(err_msg)
      raise LaboroError(err_msg) from err

  @Module.laboro_method
  def remote_mirror(self, local_dir, remote_dir, exit_on_error=True):
    """Make a remote copy of a local directory recursively.

    Arguments:
      ``local_dir``: String. The local directory full path.
      ``remote_dir``: String. The remote directory full path.
      ``exit_on_error``: Boolean. When set to ``False``, transfer errors are ignored. If set to ``True``, raise error at first transfer error. Default to ``True``.
    """
    if not self.connected:
      self._connect()
    wksppath_ptn = re.compile(f"^{self.context.workspace.workspace_path}")
    wkspdir_ptn = re.compile(f"^{self.context.workspace.workspace_dir}")
    r_dir = re.sub(wksppath_ptn, "", local_dir)
    r_dir = re.sub(wkspdir_ptn, "", r_dir)
    r_dir = os.path.join(remote_dir, r_dir)
    for l_file in self.list_local_dir(local_dir=local_dir,
                                      file_type="f",
                                      pattern=".*"):
      self.put_file(local_file=l_file,
                    remote_dir=remote_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for l_dir in self.list_local_dir(local_dir=local_dir,
                                     file_type="d",
                                     pattern=".*"):
      self.remote_mirror(local_dir=l_dir,
                         remote_dir=os.path.join(r_dir,
                                                 os.path.basename(l_dir)),
                         exit_on_error=exit_on_error)

  @Module.laboro_method
  def delete_remote_file(self, remote_file, exit_on_error=True):
    """
    Delete specified file from remote server.

    Arguments:
      ``remote_file``: The remote filepath to delete.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    self.context.log.info(f"Deleting remote file: {remote_file}")
    try:
      self.client.delete(remote_file)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        self.context.log.critical(err_msg)
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  @Module.laboro_method
  def delete_remote_dir(self, remote_dir, recursive=False, exit_on_error=True):
    """
    Delete specified  directory from remote server.

    Arguments:
      ``remote_dir``: The remote directory to delete.
      ``recursive``: If set to ``True``, delete directory and all its content.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    if not self.connected:
      self._connect()
    self.context.log.info(f"Deleting remote directory: {remote_dir}")
    try:
      for r_file in self.list_remote_dir(remote_dir=remote_dir):
        self.delete_remote_file(remote_file=r_file)
      if recursive:
        for r_dir in self.list_remote_dir(remote_dir=remote_dir, file_type="d"):
          self.delete_remote_dir(remote_dir=r_dir,
                                 recursive=recursive,
                                 exit_on_error=exit_on_error)
      self.client.rmd(remote_dir)
    except Exception as err:
      err_msg = f"[FtpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        self.context.log.critical(err_msg)
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  def _create_remote_dirs(self, remote_dir, exit_on_error=True):
    """
    Create the specified directory structure on the remote host.

    Arguments:
      ``remote_dir``: String. The remote directory full path to create.
    """
    if not self.connected:
      self._connect()
    hierarchy = [d for d in remote_dir.split("/") if len(d) > 0]
    self.context.log.info(f"Creating remote dir: {remote_dir}")
    r_dir = "/"
    while len(hierarchy) > 0:
      r_dir = os.path.join(r_dir, hierarchy.pop(0))
      rmt_dir = os.path.dirname(r_dir)
      if f"{r_dir}" not in self.list_remote_dir(remote_dir=rmt_dir,
                                                file_type="d"):
        try:
          self.client.mkd(r_dir)
        except Exception as err:
          err_msg = f"[FtpCreateDirError] {err.__class__.__name__}: {err}"
          if exit_on_error:
            self.context.log.critical(err_msg)
            raise LaboroError(err_msg) from err
          self.context.log.warning(err_msg)
