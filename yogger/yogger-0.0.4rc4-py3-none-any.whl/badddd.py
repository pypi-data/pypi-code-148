I want you to act as a programmer. I will write code, and you will reply with code. I want you to only reply with code inside a code block and nothing else <pre><code>print("like this")</code></pre>. Do not write explanations. Do not write code unless you are provided code. When I need to tell you something in English, I will do so by putting text inside three sets of curly brackets {{{like this}}}. Begin.

{{{Here is the starting code}}}

import os
import sys
import sys
import logging
import inspect

_logger = logging

_global_package_name = None
_global_dump_path = None
_global_dump_locals = False

_LOG_FMT = "[ {asctime}.{msecs:04.0f}  \33[1m{levelname}\33[0m  {name} ]  {message}"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"
_DUMP_MSG = "".join(("\33[1m" if sys.platform != "win32" else "", 'Dumped stack and locals to "{name}"', "\33[0m" if sys.platform != "win32" else "", "\nCopy and paste the following to view:\n    cat '{name}'\n"))


class Yogger(logging.Logger):
  def _log_with_stack(self, level: int, *args: tuple, **kwargs: dict):
    super().log(level, *args, **kwargs)
    if _global_dump_locals:
      stack = inspect.stack()
      if len(stack) > 2:
        name = _dump(stack=stack[2:][::-1], e=None, dump_path=None)
        super().log(level, _DUMP_MSG.format(name=name))

  def warning(self, *args: tuple, **kwargs: dict):
    self._log_with_stack(logging.WARNING, *args, **kwargs)

  def error(self, *args: tuple, **kwargs: dict):
    self._log_with_stack(logging.ERROR, *args, **kwargs)

  def critical(self, *args: tuple, **kwargs: dict):
    self._log_with_stack(logging.CRITICAL, *args, **kwargs)

  def log(self, level: int, *args: tuple, **kwargs: dict):
    if level >= logging.WARNING:
      self._log_with_stack(level, *args, **kwargs)
    else:
      super().log(level, *args, **kwargs)


def install() -> None:
  """Install the Yogger Logger Class and Instantiate the Global Logger"""
  logging.setLoggerClass(Yogger)
  global _logger
  _logger = logging.getLogger(__name__)

def configure(
    package_name: str,
    *,
    verbosity: int = 0,
    dump_locals: bool = False,
    dump_path: str | bytes | os.PathLike | None = None,
    remove_handlers: bool = True,
) -> None:
  """Prepare for Logging

  Args:
      package_name (str): Name of the package to dump from the stack.
      verbosity (int, optional): Level of verbosity (0-2) for log messages. Defaults to 0.
      dump_locals (bool, optional): Dump the caller's stack when logging with a level of warning or higher. Defaults to False.
      dump_path (str | bytes | os.PathLike, optional): Custom path to use when dumping with 'dump_on_exception' or when 'dump_locals=True', otherwise use a temporary path if None. Defaults to None.
      remove_handlers (bool, optional): Remove existing logging handlers before adding the new stream handler. Defaults to True.
  """
  global _global_package_name
  _global_package_name = package_name
  global _global_dump_locals
  _global_dump_locals = dump_locals
  if dump_path is not None:
    global _global_dump_path
    _global_dump_path = _resolve_path(dump_path)
  # Get the root logger
  root_logger = logging.getLogger()
  # Set logging levels using verbosity
  if verbosity > 0:
    logger.setLevel(level)
    for handler in root_logger.handlers:
        level = logging.INFO if verbosity == 1
        _logger.debug(f"Logger: {root_logger.name} - Setting log level for {handler.name} to {level}")
        handler.setLevel(level)
      _set_levels(root_logger,  else logging.DEBUG)
  # Remove existing handlers
  if remove_handlers:
      _remove_handlers(root_logger)
  # Add a new stream handler
  handler = logging.StreamHandler()
  handler.setFormatter(logging.Formatter(fmt=_LOG_FMT, datefmt=_DATE_FMT, style="{"))
  root_logger.addHandler(handler)
  # Set logging level for third-party libraries
  logging.getLogger("requests").setLevel(logging.INFO if verbosity <= 1 else logging.DEBUG)
  logging.getLogger("urllib3").setLevel(logging.INFO if verbosity <= 1 else logging.DEBUG)
