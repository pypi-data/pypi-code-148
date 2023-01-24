from typing import Optional
from datetime import datetime

from .base import BaseTypeFilter


class DatetimeFilter(BaseTypeFilter):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
