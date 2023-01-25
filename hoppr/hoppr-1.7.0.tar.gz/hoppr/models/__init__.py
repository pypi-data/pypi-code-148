"""
Base model for Hoppr config files
"""
from __future__ import annotations

from pydantic import Field

from hoppr.models.base import HopprBaseModel
from hoppr.models.credentials import Credentials, CredentialsFile
from hoppr.models.manifest import Manifest, ManifestFile
from hoppr.models.transfer import Transfer, TransferFile

__all__ = [
    "Credentials",
    "CredentialsFile",
    "HopprBaseModel",
    "Manifest",
    "ManifestFile",
    "Transfer",
    "TransferFile",
]


class HopprSchemaModel(HopprBaseModel):
    """
    Consolidated Hoppr config file schema definition
    """

    __root__: CredentialsFile | ManifestFile | TransferFile = Field(..., discriminator="kind")


class HopprData(HopprBaseModel):
    """
    Consolidated Hoppr config file data model
    """

    credentials: Credentials | None = Field(None)
    manifest: Manifest = Field(...)
    transfer: Transfer = Field(...)
