"""Configuration for the module."""
import os

from logging import INFO  # change it to DEBUG for more information

try:
    import dotenv
except ImportError:
    print("Warning: dotenv package not installed.")
    dotenv = None

# Current Root Path
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/config")[0])

# OVERRIDE GLOBAL VARIABLES
PACKAGE_NAME = None   # NOTE might be insecure to override

# OVERRIDE LOGGER VARIABLES
DEFAULT_LOGGER_NAME = "main_log"   # main logger name
LOGGER_LEVEL = INFO                # logger level
LOGGER_DIR = ROOT_DIR + "/logger"  # logger directory
LOGGER_FORMAT = "simple"           # logger format

# Package Environment Variables
if dotenv is not None:
    dotenv.load_dotenv()
    PACKAGE_NAME = str(os.getenv('PACKAGE_NAME'))