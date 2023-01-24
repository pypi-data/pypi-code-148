"""Strangeworks SDK."""

import importlib.metadata

from .core.config import config
from .sw_client import SWClient

__version__ = importlib.metadata.version("strangeworks")

cfg = config.Config()
client = SWClient(cfg=cfg)  # instantiate a client on import by default

# strangeworks.(public method)
authenticate = client.authenticate
workspace_info = client.workspace_info
resources = client.resources
execute = client.execute
jobs = client.jobs
upload_file = client.upload_file
backends = client.get_backends
