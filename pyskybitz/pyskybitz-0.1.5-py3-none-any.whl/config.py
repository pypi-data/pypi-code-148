"""Configurations."""
from pydantic import BaseModel


class ConnectionConfig(BaseModel):
    """Credentials to connect to API."""

    customer: str
    password: str
    port: int
    base_domain: str
    version: str
