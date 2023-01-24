from typing import Optional
from .base import BaseTypeFilter


class NumberFilter(BaseTypeFilter):
    equal: Optional[int] = None
    gt: Optional[int] = None
    lt: Optional[int] = None
