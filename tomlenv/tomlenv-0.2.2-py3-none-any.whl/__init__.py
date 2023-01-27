__all__ = ("DataclassError", "ConfigError", "Parser")

from ._parser import ConfigError, DataclassError, Parser

# Pretend this exception was created here.
DataclassError.__module__ = __name__
ConfigError.__module__ = __name__
