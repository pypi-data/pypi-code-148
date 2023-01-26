import logging

from fraud_analysis.config.core import PACKAGE_ROOT, config

# This file __init__.py is only run once
# the very first time I import anything from fraud_analysis package
# Once I reach "from fraud_analysis.config.core import PACKAGE_ROOT, config"
# I will run the __init__,py inside the config subpackage, and then core.py
# I won't go back to this __init__.py until the entire core.py is run.

# It is strongly advised that you do not add any handlers other than
# NullHandler to your library’s loggers. This is because the configuration
# of handlers is the prerogative of the application developer who uses your
# library. The application developer knows their target audience and what
# handlers are most appropriate for their application: if you add handlers
# ‘under the hood’, you might well interfere with their ability to carry out
# unit tests and deliver logs which suit their requirements.
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger(config.app_config.package_name).addHandler(logging.NullHandler())

with open(PACKAGE_ROOT / "VERSION") as version_file:
    __version__ = version_file.read().strip()
