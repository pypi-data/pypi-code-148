"""This module contains type aliases and data types for type hints"""

__all__ = ["RealMatrix", "RealVector", "SampleSize", "UncertainArray"]

from typing import NamedTuple, TypeAlias

import numpy as np
from numpy._typing import NDArray

RealMatrix: TypeAlias = NDArray[np.float64]
"""A real matrix represented by a :class:`np.ndarray <numpy.ndarray>`"""
RealVector: TypeAlias = NDArray[np.float64]
"""A real vector represented by a :class:`np.ndarray <numpy.ndarray>`"""


class UncertainArray(NamedTuple):
    """A tuple of a tensor of values with a tensor of associated uncertainties"""

    values: RealVector
    """the corresponding values"""
    uncertainties: RealMatrix | RealVector
    """... and their associated uncertainties"""


class SampleSize(NamedTuple):
    """A tuple to specify the size of the extracted data"""

    idx_first_cycle: int = 0
    """index of first sample to be extracted

    defaults to 0 and must be between 0 and 4765
    """
    n_cycles: int = 1
    """number of cycles extracted from the dataset

    each cycle contains the first :attr:`datapoints_per_cycle` readings from each of
    the eleven sensors for one of the cycles with associated standard uncertainties,
    defaults to 1 and must be between 1 and 4766 - :attr:`idx_first_cycle`"""
    datapoints_per_cycle: int = 1
    """number of sensor readings from each of the individual sensors per sample/cycle

    defaults to 1 and should be between 1 and 2000, as there are only 2000 readings
    per cycle, higher values will be clipped to 2000
    """
