"""Maintain constant size complexity and evenly-spaced strata.

The depth-proportional resolution policy ensures estimates of MRCA rank will
have uncertainty bounds less than or equal to a user-specified proportion of
the largest number of strata deposited on either column. Thus, MRCA rank
estimate uncertainty scales as O(n) with respect to the greater number of
strata deposited on either column.

Under the depth-proportional resolution policy, the number of strata retained
(i.e., space complexity) scales as O(1) with respect to the number of strata
deposited.

This retention policy guarantees that columns will retain appropriate strata so
that for any two columns with m and n strata deposited, the rank of the most
recent common ancestor can be determined with uncertainty of at most

    bound = floor(max(m, n) / depth_proportional_resolution)

ranks. Achieving this limit on uncertainty requires retaining sufficient strata
so that no more than bound ranks elapsed between any two strata. This policy
accumulates retained strata at a fixed interval until twice as many as
depth_proportional_resolution are at hand. Then, every other
retained stratum is purged and the cycle repeats with a new twice-as-wide
interval between retained strata.

Suppose depth_proportional_resolution is 3.

       guaranteed   actual
time   resolution   uncertainty   column
--------------------------------------------------------
1      0            0             |
2      0            0             ||
3      1            0             |||
4      1            0             ||||
5      1            0             |||||
6      2            2             | | ||
7      2            2             | | | |
8      2            2             | | | ||
9      3            2             | | | | |
10     3            2             | | | | ||
11     3            2             | | | | | |
12     4            4             |   |   |  |
13     4            4             |   |   |   |
14     4            4             |   |   |   ||
15     5            4             |   |   |   | |
16     5            4             |   |   |   |  |
17     5            4             |   |   |   |   |
18     6            4             |   |   |   |   ||
19     6            4             |   |   |   |   | |
20     6            4             |   |   |   |   |  |
21     7            4             |   |   |   |   |   |
22     7            4             |   |   |   |   |   ||
23     7            4             |   |   |   |   |   | |
24     8            8             |       |       |      |
25     8            8             |       |       |       |
26     8            8             |       |       |       ||
27     9            8             |       |       |       | |
28     9            8             |       |       |       |  |
29     9            8             |       |       |       |   |

See Also
--------
depth_proportional_resolution_tapered_algo:
    For a retention policy that achieves the same guarantees for depth-
    proportional resolution but purges unnecessary strata more graudally.
"""

from ._Policy import Policy
from ._PolicySpec import PolicySpec
from ._enact._GenDropRanks import GenDropRanks
from ._enact._GenDropRanks_ import impls as _GenDropRanks_impls
from ._invar._CalcMrcaUncertaintyAbsUpperBound import (
    CalcMrcaUncertaintyAbsUpperBound,
)
from ._invar._CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank import (
    CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank,
)
from ._invar._CalcMrcaUncertaintyAbsUpperBoundPessimalRank import (
    CalcMrcaUncertaintyAbsUpperBoundPessimalRank,
)
from ._invar._CalcMrcaUncertaintyRelUpperBound import (
    CalcMrcaUncertaintyRelUpperBound,
)
from ._invar._CalcMrcaUncertaintyRelUpperBoundAtPessimalRank import (
    CalcMrcaUncertaintyRelUpperBoundAtPessimalRank,
)
from ._invar._CalcMrcaUncertaintyRelUpperBoundPessimalRank import (
    CalcMrcaUncertaintyRelUpperBoundPessimalRank,
)
from ._invar._CalcNumStrataRetainedUpperBound import (
    CalcNumStrataRetainedUpperBound,
)
from ._scry._CalcMrcaUncertaintyAbsExact import CalcMrcaUncertaintyAbsExact
from ._scry._CalcMrcaUncertaintyRelExact import CalcMrcaUncertaintyRelExact
from ._scry._CalcNumStrataRetainedExact import CalcNumStrataRetainedExact
from ._scry._CalcRankAtColumnIndex import CalcRankAtColumnIndex
from ._scry._IterRetainedRanks import IterRetainedRanks

__all__ = [
    "CalcMrcaUncertaintyAbsExact",
    "CalcMrcaUncertaintyAbsUpperBound",
    "CalcMrcaUncertaintyAbsUpperBoundAtPessimalRank",
    "CalcMrcaUncertaintyAbsUpperBoundPessimalRank",
    "CalcMrcaUncertaintyRelExact",
    "CalcMrcaUncertaintyRelUpperBound",
    "CalcMrcaUncertaintyRelUpperBoundAtPessimalRank",
    "CalcMrcaUncertaintyRelUpperBoundPessimalRank",
    "CalcNumStrataRetainedExact",
    "CalcNumStrataRetainedUpperBound",
    "CalcRankAtColumnIndex",
    "GenDropRanks",
    "_GenDropRanks_impls",
    "IterRetainedRanks",
    "Policy",
    "PolicySpec",
]

from ...._auxiliary_lib import launder_impl_modules as _launder

_launder([eval(item) for item in __all__], __name__)
del _launder  # prevent name from leaking
