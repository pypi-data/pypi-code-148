import os
import re
import stat
import socket
import logging
import paramiko
from laboro.error import LaboroError
from laboro.module import Module

logging.captureWarnings(True)
paramiko_logger = paramiko.util.get_logger("paramiko")
paramiko_logger.disabled = True
paramiko_transport_logger = logging.getLogger("paramiko.transport")
paramiko_transport_logger.disabled = True


class Ssh(Module):
  """This class is derived from the ``laboro.module.Module`` base class.

  Its purpose is to provide a SSH/SFTP client able to execute commands and transfer files using the SSH protocol.

  Arguments:

    args: An optional dictionary representing all module args, their types and their values.

    ``username``: String. The user name to use for authentication on remote host.
    ``password``: String. Optional, the password to use fo authentication on remote host. If the ``key`` argument is provided, then the ``password`` value will be use as the SSH key passphrase.
    ``host``: String. The remote host to connect to.
    ``port``: Int. Optional. The TCP remote port to connect to. Default: ``22``.
    ``key``: String. Optional. The SSH private key file name to use for authentication on remote host.
    ``missing_host_key_policy``: String. Optional. Define the behavior when a remote key is missing and remote host is unknown. This should be one of ``auto``, ``warn``, ``reject``. Default to ``warn`` which automatically add remote host key to the known keys and log a warning.

    Note:
      - When the ``password`` argument is provided alongside the ``key`` argument then it will be assumed that the provided password is a passphrase for the specified key.
      - The ``missing_host_key_policy`` allow one of the 4 following values:
        - ``auto``: Automatically add remote host key to the known keys.
        - ``warning``: Same as auto and log a warning.
        - ``reject``: Reject the host key, do not proceed to connection and raise an error resulting in the immediate exit of the workflow.
  """
  @property
  def connected(self):
    if self.client is not None and self.client.get_transport() is not None:
      return self.client.get_transport().is_active()
    return False

  @property
  def sftp(self):
    """
    Open a SFTP transport connection to remote host.
    """
    if not self.connected:
      self._connect()
    if self.sftp_client is None:
      self.sftp_client = self.client.open_sftp()
    return self.sftp_client

  def __init__(self, context, args=None):
    super().__init__(filepath=__file__, context=context, args=args)
    self.client = None
    self.sftp_client = None

  def __enter__(self):
    super().__enter__()
    self._connect()
    return self

  def __exit__(self, type_err, value, traceback):
    self._close()

  def _connect(self):
    self.context.log.info(f"Connecting to {self.args.get('host')}:{self.args.get('port')}")
    self.client = paramiko.SSHClient()
    self.client.set_log_channel("laboro.ssh_transport")
    self.client.set_missing_host_key_policy(
        self._get_missing_key_policy(
            self.args.get("missing_host_key_policy")))
    self.client.load_system_host_keys()
    try:
      self.client.connect(hostname=self.args.get("host"),
                          port=self.args.get("port"),
                          username=self.args.get("username"),
                          password=self.args.get("password"),
                          key_filename=self.args.get("key"))
    except (paramiko.ssh_exception.BadHostKeyException,
            paramiko.ssh_exception.AuthenticationException,
            paramiko.ssh_exception.SSHException,
            socket.error,
            socket.gaierror,
            paramiko.ssh_exception.NoValidConnectionsError) as err:
      raise LaboroError(f"[SshConnectionError] {err.__class__.__name__}: {err}") from err

  def _close(self):
    self.context.log.info(f"Closing connection to {self.args.get('host')}:{self.args.get('port')}")
    if self.connected:
      self.client.close()

  def _get_missing_key_policy(self, key):
    policies = {"auto": paramiko.client.AutoAddPolicy(),
                "warn": paramiko.client.WarningPolicy(),
                "reject": paramiko.client.RejectPolicy()}
    try:
      return policies[key]
    except KeyError as err:
      raise LaboroError(f"[SshUnknownPolicyError] Unknown 'missing key policy': {key}") from err

  def _log_line(self, line, buffer, level):
    if len(line) > 0:
      buffer.append(line)
      self.context.log.log(level, line)

  @Module.laboro_method
  def exec(self, command, exit_on_error=True):
    """
    Execute the specified command on the remote host.

    Arguments:
    ``command``: String. The command to be executed on the remote host.
    ``exit_on_error``: Boolean. Optional,  Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.

    Returns:
      ``dict``: A dictionary containing the following items:
                - ``exit_code``: The exit code returned by the command.
                - ``stdout``: A list containing each line of the standard output returned by the command.
                - ``stderr``: A list containing each line of the standard error returned by the command.
    """
    if not self.connected:
      self._connect()
    self.context.log.info(f"Running command: {command}")
    try:
      exit_code = None
      stdin, stdout, stderr = self.client.exec_command(command)
      channel = stdout.channel
      stdout_content = list()
      stderr_content = list()
      while True:
        while channel.recv_ready():
          self._log_line(line=stdout.readline().strip(),
                         buffer=stdout_content,
                         level=logging.INFO)
        while channel.recv_stderr_ready():
          self._log_line(line=stderr.readline().strip(),
                         buffer=stderr_content,
                         level=logging.ERROR)
        if channel.exit_status_ready():
          self._log_line(line=stdout.readline().strip(),
                         buffer=stdout_content,
                         level=logging.INFO)
          self._log_line(line=stderr.readline().strip(),
                         buffer=stderr_content,
                         level=logging.ERROR)
          exit_code = channel.recv_exit_status()
          break
      if exit_code > 0:
        raise LaboroError(f"[SshExecError] {' '.join(stderr_content)}")
      return {"exit_code": exit_code,
              "stdout": stdout_content,
              "stderr": stderr_content}
    except LaboroError as err:
      self.context.log.error(str(err))
      if not exit_on_error:
        return {"exit_code": exit_code,
                "stdout": stdout_content,
                "stderr": stderr_content}
      raise LaboroError(str(err)) from err
    except paramiko.SSHException as err:
      err_msg = f"[SshExecError] {err.__class__.__name__}: {err}"
      if exit_on_error:
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

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
    local_dir = local_dir.rstrip("/")
    local_fname = os.path.join(local_dir, os.path.basename(remote_file))
    if create_dirs:
      local_fname = os.path.join(local_dir, remote_file.lstrip("/"))
      self._create_local_dirs(remote_file, local_dir)
    self.context.log.info(f"Getting remote file: {remote_file}")
    try:
      self.sftp.get(remote_file, local_fname)
    except Exception as err:
      err_msg = f"[SftpTransferError] {err.__class__.__name__} {err}"
      if exit_on_error:
        self.context.log.critical(err_msg)
        raise LaboroError(err_msg) from err
      self.context.log.warning(err_msg)

  @Module.laboro_method
  def put_file(self, local_file, remote_dir,
               create_dirs=False, exit_on_error=True):
    """
    Send local file ``local_file`` to remote directory ``remote_dir``.
    If ``create_dirs`` is set to ``True``, a directory structure matching the local directory hierarchy will be created on the remote host.

    Arguments:
      ``local_file``: String. Local filename full path.
      ``remote_dir``: String. Remote directory where to store the file.
      ``create_dirs``: Boolean. Optional. Create all missing directory components found in ``remote_dir``. Default: ``False``.
      ``exit_on_error``: Boolean. Optional. If set to ``False``, any error encountered will only be logged as a warning. Default: ``True``.
    """
    remote_dir = remote_dir.rstrip("/")
    remote_fname = os.path.join(remote_dir, os.path.basename(local_file))
    self.context.log.info(f"Sending file to: {remote_fname}")
    if create_dirs:
      self._create_remote_dirs(remote_dir=remote_dir,
                               exit_on_error=exit_on_error)
    try:
      self.sftp.put(local_file, remote_fname, confirm=True)
    except Exception as err:
      err_msg = f"[SftpTransferError] {err.__class__.__name__} {err}"
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
      err_msg = f"[SshLocalOSError] {err.__class__.__name__} {err}"
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
    for r_file in self.list_remote_dir(remote_dir=remote_dir,
                                       file_type="f", pattern=".*"):
      self.get_file(remote_file=os.path.join(remote_dir, r_file),
                    local_dir=local_dir,
                    create_dirs=True,
                    exit_on_error=exit_on_error)
    for r_dir in self.list_remote_dir(remote_dir=remote_dir,
                                      file_type="d", pattern=".*"):
      self.local_mirror(remote_dir=os.path.join(remote_dir, r_dir),
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
      err_msg = f"[SshLocalOSError] {err.__class__.__name__}: {err}"
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
      err_msg = f"[SshLocalOSError] {err.__class__.__name__}: {err}"
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
      err_msg = f"[SftpLocalOSError] {err.__class__.__name__} {err}"
      self.context.log.error(err_msg)
      raise LaboroError(err_msg) from err

# -----------------------------------------------------------------------------
# Remote operations
# -----------------------------------------------------------------------------
  @Module.laboro_method
  def list_remote_dir(self, remote_dir, file_type="f", pattern=".*"):
    """
    Get the complete list of files or dirs found in the specified remote directory and matching the specified file type (f or d) and the specified regular expression pattern.

    Note: This method is **NOT** recursive.

    Arguments:
      ``remote_dir``: String. Optional. The full path of the remote directory to explore.
      ``file_type``: String. Optional. If set to ``d``, the returned list will only contain directory names. When set to ``f``, the returned list will contain only file names. Default: ``f``.
      pattern: String. A regular expression to filter returned values. Default to ``.*``
    """
    dirs = list()
    files = list()
    if len(remote_dir) > 1:
      remote_dir = remote_dir.rstrip("/")
    reg = re.compile(pattern)
    self.context.log.info(f"Exploring {remote_dir}")
    try:
      for f in self.sftp.listdir_attr(remote_dir):
        if re.match(reg, f.filename):
          if stat.S_ISDIR(f.st_mode):
            dirs.append(f.filename)
          elif stat.S_ISREG(f.st_mode):
            files.append(f.filename)
          elif stat.S_ISLNK(f.st_mode):
            l_stat = self.sftp.stat(os.path.join(remote_dir, f.filename))
            if stat.S_ISDIR(l_stat.st_mode):
              dirs.append(f.filename)
            elif stat.S_ISREG(l_stat.st_mode):
              files.append(f.filename)
      if file_type == "f":
        return files
      elif file_type == "d":
        return dirs
    except Exception as err:
      err_msg = f"[SshRemoteOSError] {err.__class__.__name__} {err}"
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
                         remote_dir=os.path.join(remote_dir,
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
    self.context.log.info(f"Deleting remote file: {remote_file}")
    try:
      self.sftp.remove(remote_file)
    except Exception as err:
      err_msg = f"[SftpRemoteOSError] {err.__class__.__name__} {err}"
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
    self.context.log.info(f"Deleting remote directory: {remote_dir}")
    try:
      for r_file in self.list_remote_dir(remote_dir=remote_dir):
        r_file = os.path.join(remote_dir, r_file)
        self.delete_remote_file(remote_file=r_file)
      if recursive:
        for r_dir in self.list_remote_dir(remote_dir=remote_dir, file_type="d"):
          r_dir = os.path.join(remote_dir, r_dir)
          self.delete_remote_dir(remote_dir=r_dir,
                                 recursive=recursive,
                                 exit_on_error=exit_on_error)
      self.sftp.rmdir(remote_dir)
    except Exception as err:
      err_msg = f"[SftpRemoteOSError] {err.__class__.__name__} {err}"
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
    hierarchy = [d for d in remote_dir.split("/") if len(d) > 0]
    self.context.log.info(f"Creating remote dir: {remote_dir}")
    r_dir = "/"
    while len(hierarchy) > 0:
      r_dir = os.path.join(r_dir, hierarchy.pop(0))
      rmt_dir = os.path.dirname(r_dir)
      if os.path.basename(r_dir) not in self.list_remote_dir(remote_dir=rmt_dir,
                                                             file_type="d"):
        try:
          self.sftp.mkdir(r_dir)
        except Exception as err:
          err_msg = f"[SftpRemoteOSError] {err.__class__.__name__}: {err}"
          if exit_on_error:
            self.context.log.critical(err_msg)
            raise LaboroError(err_msg) from err
          self.context.log.warning(err_msg)
