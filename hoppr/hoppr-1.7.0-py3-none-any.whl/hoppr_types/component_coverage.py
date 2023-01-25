"""
Enumeration to indicate how often each component should be processed
"""
import math

from enum import Enum


class ComponentCoverage(Enum):
    """
    Enumeration to indicate how often each component should be processed
    """

    OPTIONAL = (0, math.inf)
    EXACTLY_ONCE = (1, 1)
    AT_LEAST_ONCE = (1, math.inf)
    NO_MORE_THAN_ONCE = (0, 1)

    def __init__(self, min_allowed: int, max_allowed: int):
        self.min_value = min_allowed
        self.max_value = max_allowed

    def accepts_count(self, count: int) -> bool:
        """
        Identifies whether a specified count is acceptable for this coverage value
        """
        return self.min_value <= count <= self.max_value
