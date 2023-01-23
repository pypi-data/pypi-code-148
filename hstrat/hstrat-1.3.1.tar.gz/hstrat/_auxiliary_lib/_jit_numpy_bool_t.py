"""Provides numba bool type or numpy bool type.

Type must be declared outside jit'ed function or numba fails.
"""

import numpy as np

from ._is_in_coverage_run import is_in_coverage_run

try:
    import numba as nb
except ImportError:
    jit_numpy_bool_t = np.bool_
else:
    if is_in_coverage_run():
        # when numba disabled for coverage testing,
        # using nb.types.bool_ causes numpy TypeError
        jit_numpy_bool_t = np.bool_
    else:
        jit_numpy_bool_t = nb.types.bool_
