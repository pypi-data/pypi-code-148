import os
from logging import INFO
from .. import __about__

class LoggerDef():
    """Default values for the logger config."""
    ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])
    LEVEL = INFO                        
    DIRECTORY = f'{ROOT_DIR}/logger'    
    FORMAT = 'simple'                   
    NAME = 'main_log'
    TYPE = 'default'

class PackageDef():
    """Default values for the package config."""
    NAME = 'probable_fiesta'

class VariablesDef():
    """Default values for the variables config."""
    VERSION = __about__.__version__

class DotEnvDef():
    """Default values for the dotenv config."""
    # This has precedence over the PackageDefaults
    def __init__(self):
        self.PACKAGE_NAME = 'probable_fiesta'
        self.PACKAGE_VERSION = '0.0.1'
        # Add more variables here
    
    def __iter__(self):
        return iter(self.__dict__)