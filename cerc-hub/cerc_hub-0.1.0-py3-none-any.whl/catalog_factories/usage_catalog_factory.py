"""
Usage catalog factory, publish the usage information
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""

from pathlib import Path
from typing import TypeVar
from catalog_factories.usage.comnet_catalog import ComnetCatalog
from catalog_factories.usage.nrcan_catalog import NrcanCatalog
Catalog = TypeVar('Catalog')


class UsageCatalogFactory:
  def __init__(self, file_type, base_path=None):
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/usage')
    self._catalog_type = '_' + file_type.lower()
    self._path = base_path

  @property
  def _comnet(self):
    """
    Retrieve Comnet catalog
    """
    return ComnetCatalog(self._path)

  @property
  def _nrcan(self):
    """
    Retrieve NRCAN catalog
    """
    # nrcan retrieves the data directly from github
    return NrcanCatalog(self._path)

  @property
  def catalog(self) -> Catalog:
    """
    Enrich the city given to the class using the class given handler
    :return: Catalog
    """
    return getattr(self, self._catalog_type, lambda: None)
