from typing import Optional

from .base import BaseTypeFilter


class StringFilter(BaseTypeFilter):
    includes: Optional[str] = None
    exact: Optional[str] = None
    begin: Optional[str] = None
    end: Optional[str] = None
