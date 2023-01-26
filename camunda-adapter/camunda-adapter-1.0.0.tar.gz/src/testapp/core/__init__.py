"""Ядро пиложения."""

from typing import Union

from camunda_adapter.adapters import Adapter
from camunda_adapter.config import Config


# Предоставляются при инициализации
config: Union[Config, None] = None
adapter: Union[Adapter, None] = None
