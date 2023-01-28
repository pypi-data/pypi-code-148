from typing import Optional
from .base import BaseTypeFilter


class ExistsFilter(BaseTypeFilter):
    exists: Optional[bool] = None
