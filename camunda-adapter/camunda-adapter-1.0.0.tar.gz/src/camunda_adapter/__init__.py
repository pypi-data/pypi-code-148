"""Пакет содержит адаптер к платформе Camunda и инструменты для его работы."""

from .adapters import Adapter
from .config import Config


__all__ = [
    'Adapter',
    'Config'
]
