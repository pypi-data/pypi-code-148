import random

import pytest

from hstrat import hstrat


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
def test_col_to_dataframe(
    retention_policy,
):
    pop = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_retention_policy=retention_policy,
        )
        for __ in range(10)
    ]
    for __ in range(100):
        target = random.randrange(len(pop))
        pop[target] = random.choice(pop).CloneDescendant()

    df = hstrat.pop_to_dataframe(pop)

    assert len(df) == sum(column.GetNumStrataRetained() for column in pop)
    for col_idx, col_df in df.groupby("column"):
        assert (
            col_df.drop(
                "column",
                axis=1,
            )
            .reset_index(
                drop=True,
            )
            .equals(
                hstrat.col_to_dataframe(pop[col_idx]),
            )
        )
