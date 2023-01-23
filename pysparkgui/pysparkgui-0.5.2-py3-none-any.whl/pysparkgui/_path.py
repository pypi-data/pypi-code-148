# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

from os.path import dirname
from pathlib import Path

pysparkgui_LIBRARY_ROOT_PATH = Path(dirname(__file__))

USER_HOME_PATH = Path.home()
pysparkgui_LIBRARY_CONFIG_PATH = USER_HOME_PATH / ".pysparkgui"
pysparkgui_LIBRARY_INTERNAL_CONFIG_PATH = pysparkgui_LIBRARY_CONFIG_PATH / "__internal__"

# ATTENTION: This is the base path used by pandas and os.
# If you need a base path for pyspark (starts with "dbfs:/"), create a new constant
DBFS_BASE_PATH = Path("/dbfs/FileStore")
