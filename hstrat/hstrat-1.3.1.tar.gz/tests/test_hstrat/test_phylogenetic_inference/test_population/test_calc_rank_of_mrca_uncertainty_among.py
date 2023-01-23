import itertools as it
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
@pytest.mark.parametrize(
    "ordered_store",
    [
        hstrat.HereditaryStratumOrderedStoreDict,
        hstrat.HereditaryStratumOrderedStoreList,
        pytest.param(
            hstrat.HereditaryStratumOrderedStoreTree,
            marks=pytest.mark.heavy,
        ),
    ],
)
def test_comparison_commutativity_asyncrhonous(
    retention_policy,
    ordered_store,
):
    population = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_ordered_store=ordered_store,
            stratum_retention_policy=retention_policy,
        )
        for __ in range(10)
    ]

    for generation in range(100):
        for first, second in it.combinations(population, 2):
            # assert commutativity
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among([first, second])
                == hstrat.calc_rank_of_mrca_uncertainty_among([second, first])
                == hstrat.calc_rank_of_mrca_uncertainty_among(
                    [second, first, first]
                )
                == hstrat.calc_rank_of_mrca_uncertainty_among(
                    [second, first] * 3
                )
            )

        # advance generation
        random.shuffle(population)
        for target in range(5):
            population[target] = population[-1].CloneDescendant()
        for individual in population:
            # asynchronous generations
            if random.choice([True, False]):
                individual.DepositStratum()


@pytest.mark.parametrize(
    "retention_policy",
    [
        pytest.param(
            hstrat.perfect_resolution_algo.Policy(),
            marks=pytest.mark.heavy_2a,
        ),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
@pytest.mark.parametrize(
    "ordered_store",
    [
        pytest.param(
            hstrat.HereditaryStratumOrderedStoreDict,
            marks=pytest.mark.heavy_2b,
        ),
        hstrat.HereditaryStratumOrderedStoreList,
        pytest.param(
            hstrat.HereditaryStratumOrderedStoreTree,
            marks=pytest.mark.heavy,
        ),
    ],
)
def test_comparison_commutativity_syncrhonous(
    retention_policy,
    ordered_store,
):

    population = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_ordered_store=ordered_store,
            stratum_retention_policy=retention_policy,
        )
        for __ in range(10)
    ]

    for generation in range(100):

        for first, second in it.combinations(population, 2):
            # assert commutativity
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among([first, second])
                == hstrat.calc_rank_of_mrca_uncertainty_among([second, first])
                == hstrat.calc_rank_of_mrca_uncertainty_among(
                    [second, first, second]
                )
                == hstrat.calc_rank_of_mrca_uncertainty_among(
                    [second, first] * 3
                )
            )

        # advance generation
        random.shuffle(population)
        for target in range(5):
            population[target] = population[-1].Clone()
        # synchronous generations
        for individual in population:
            individual.DepositStratum()


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
@pytest.mark.parametrize(
    "ordered_store",
    [
        hstrat.HereditaryStratumOrderedStoreDict,
        hstrat.HereditaryStratumOrderedStoreList,
        pytest.param(
            hstrat.HereditaryStratumOrderedStoreTree,
            marks=pytest.mark.heavy,
        ),
    ],
)
def test_comparison_validity(retention_policy, ordered_store):
    population = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_ordered_store=ordered_store,
            stratum_retention_policy=retention_policy,
        )
        for __ in range(10)
    ]

    for generation in range(100):
        for first, second in it.combinations(population, 2):
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among([first, second])
                >= 0
            )
        for first, second, third in it.islice(
            it.combinations(population, 3), 100
        ):
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among(
                    [first, second, third]
                )
                >= 0
            )

        # advance generations asynchronously
        random.shuffle(population)
        for target in range(5):
            population[target] = population[-1].Clone()
        for individual in population:
            if random.choice([True, False]):
                individual.DepositStratum()


@pytest.mark.parametrize(
    "retention_policy1",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
@pytest.mark.parametrize(
    "retention_policy2",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
@pytest.mark.parametrize(
    "ordered_store",
    [
        hstrat.HereditaryStratumOrderedStoreDict,
        hstrat.HereditaryStratumOrderedStoreList,
        hstrat.HereditaryStratumOrderedStoreTree,
    ],
)
def test_scenario_no_mrca(
    retention_policy1,
    retention_policy2,
    ordered_store,
):
    first = hstrat.HereditaryStratigraphicColumn(
        stratum_ordered_store=ordered_store,
        stratum_retention_policy=retention_policy1,
    )
    second = hstrat.HereditaryStratigraphicColumn(
        stratum_ordered_store=ordered_store,
        stratum_retention_policy=retention_policy2,
    )

    for generation in range(100):
        assert hstrat.calc_rank_of_mrca_uncertainty_among([first, second]) == 0
        assert hstrat.calc_rank_of_mrca_uncertainty_among([second, first]) == 0
        assert (
            hstrat.calc_rank_of_mrca_uncertainty_among([first, second, first])
            == 0
        )
        assert (
            hstrat.calc_rank_of_mrca_uncertainty_among([second, first] * 3)
            == 0
        )

        first.DepositStratum()
        second.DepositStratum()


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.nominal_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
    ],
)
@pytest.mark.parametrize(
    "ordered_store",
    [
        hstrat.HereditaryStratumOrderedStoreDict,
        hstrat.HereditaryStratumOrderedStoreList,
        hstrat.HereditaryStratumOrderedStoreTree,
    ],
)
def test_scenario_no_divergence(retention_policy, ordered_store):
    column = hstrat.HereditaryStratigraphicColumn(
        stratum_ordered_store=ordered_store,
        stratum_retention_policy=retention_policy,
    )

    for generation in range(100):
        assert (
            hstrat.calc_rank_of_mrca_uncertainty_among([column, column]) == 0
        )
        assert (
            hstrat.calc_rank_of_mrca_uncertainty_among(
                [column, column, column]
            )
            == 0
        )
        assert (
            hstrat.calc_rank_of_mrca_uncertainty_among([column, column] * 3)
            == 0
        )

        column.DepositStratum()


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=10,
        ),
    ],
)
@pytest.mark.parametrize(
    "differentia_width",
    [1, 2, 8, 64],
)
@pytest.mark.parametrize(
    "confidence_level",
    [0.8, 0.95],
)
def test_CalcRankOfMrcaUncertaintyWith_narrow_shallow(
    retention_policy,
    differentia_width,
    confidence_level,
):

    columns = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=differentia_width,
            stratum_retention_policy=retention_policy,
            stratum_ordered_store=hstrat.HereditaryStratumOrderedStoreDict,
        )
        for __ in range(20)
    ]

    steps = list(
        range(
            columns[
                0
            ].CalcMinImplausibleSpuriousConsecutiveDifferentiaCollisions(
                significance_level=1 - confidence_level,
            )
            - columns[0].GetNumStrataDeposited()
        )
    )

    for step1, step2 in it.product(steps, steps):
        column1 = [col.Clone() for col in columns]
        column2 = [col.Clone() for col in columns]
        column3 = [col.Clone() for col in columns]
        for __ in range(step1):
            for col in column1:
                col.DepositStratum()
        for __ in range(step2):
            for col in column2:
                col.DepositStratum()
        for __ in range(step1):
            for col in column2:
                col.DepositStratum()

        for c1, c2 in zip(column1, column2):
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c1, c2], confidence_level=confidence_level
                )
                is None
            )
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c2, c1],
                    confidence_level=confidence_level,
                )
                is None
            )
        for c1, c2, c3 in zip(column1, column2, column3):
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c1, c2, c3], confidence_level=confidence_level
                )
                is None
            )
            assert (
                hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c2, c3, c1],
                    confidence_level=confidence_level,
                )
                is None
            )


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=10,
        ),
    ],
)
@pytest.mark.parametrize(
    "differentia_width",
    [1, 2, 8, 64],
)
@pytest.mark.parametrize(
    "confidence_level",
    [0.8, 0.95],
)
@pytest.mark.parametrize(
    "mrca_rank",
    [100],
)
def test_CalcRankOfMrcaUncertaintyWith_narrow_with_mrca(
    retention_policy,
    differentia_width,
    confidence_level,
    mrca_rank,
):

    columns = [
        hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=differentia_width,
            stratum_retention_policy=retention_policy,
            stratum_ordered_store=hstrat.HereditaryStratumOrderedStoreDict,
        )
        for __ in range(20)
    ]

    for generation in range(mrca_rank):
        for column in columns:
            column.DepositStratum()

    steps = (0, 16, 51)

    for step1, step2 in it.product(steps, steps):
        column1 = [col.Clone() for col in columns]
        column2 = [col.Clone() for col in columns]
        for __ in range(step1):
            for col in column1:
                col.DepositStratum()
        for i in range(step2):
            for col in column2:
                col.DepositStratum()

        for c1, c2 in zip(column1, column2):
            assert hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2], confidence_level=confidence_level
            ) == hstrat.calc_rank_of_mrca_uncertainty_among(
                [c2, c1],
                confidence_level=confidence_level,
            )
            res = hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2],
                confidence_level=confidence_level,
            )

            if res is not None:
                assert res >= 0
                assert hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c1, c2], confidence_level=confidence_level
                ) >= hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c2, c1],
                    confidence_level=confidence_level / 2,
                )

    for step1, step2 in it.product(steps, steps):
        column1 = [col.Clone() for col in columns]
        column2 = [col.Clone() for col in columns]
        column3 = [col.Clone() for col in columns]
        for __ in range(step1):
            for col in column1:
                col.DepositStratum()
        for i in range(step2):
            for col in column2:
                col.DepositStratum()
        for i in range(step1):
            for col in column3:
                col.DepositStratum()

        for c1, c2, c3 in zip(column1, column2, column3):
            assert hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2, c3], confidence_level=confidence_level
            ) == hstrat.calc_rank_of_mrca_uncertainty_among(
                [c2, c1, c3],
                confidence_level=confidence_level,
            )
            res = hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2, c3],
                confidence_level=confidence_level,
            )

            if res is not None:
                assert res >= 0
                assert hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c1, c2, c3], confidence_level=confidence_level
                ) >= hstrat.calc_rank_of_mrca_uncertainty_among(
                    [c2, c1, c3],
                    confidence_level=confidence_level / 2,
                )


@pytest.mark.parametrize(
    "retention_policy",
    [
        hstrat.perfect_resolution_algo.Policy(),
        hstrat.fixed_resolution_algo.Policy(fixed_resolution=10),
        hstrat.recency_proportional_resolution_algo.Policy(
            recency_proportional_resolution=10,
        ),
    ],
)
@pytest.mark.parametrize(
    "differentia_width",
    [1, 2, 8, 64],
)
@pytest.mark.parametrize(
    "confidence_level",
    [0.8, 0.95],
)
@pytest.mark.parametrize(
    "mrca_rank",
    [0, 100],
)
def test_CalcRankOfMrcaUncertaintyWith_narrow_no_mrca(
    retention_policy,
    differentia_width,
    confidence_level,
    mrca_rank,
):
    def make_column():
        return hstrat.HereditaryStratigraphicColumn(
            stratum_differentia_bit_width=differentia_width,
            stratum_retention_policy=retention_policy,
            stratum_ordered_store=hstrat.HereditaryStratumOrderedStoreDict,
        )

    columns = [make_column() for __ in range(20)]

    for generation in range(mrca_rank):
        for column in columns:
            column.DepositStratum()

    steps = (0, 16, 51)

    for step1, step2 in it.product(steps, steps):
        column1 = [make_column() for col in columns]
        column2 = [make_column() for col in columns]
        column3 = [make_column() for col in columns]
        for __ in range(step1):
            for col in column1:
                col.DepositStratum()
        for i in range(step2):
            for col in column2:
                col.DepositStratum()
        for i in range(step1):
            for col in column3:
                col.DepositStratum()

        for c1, c2 in zip(column1, column2):
            assert hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2], confidence_level=confidence_level
            ) == hstrat.calc_rank_of_mrca_uncertainty_among(
                [c2, c1],
                confidence_level=confidence_level,
            )
            res = hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2],
                confidence_level=confidence_level,
            )

            if res is not None:
                assert 0 <= res
                assert (
                    hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c1, c2], confidence_level=confidence_level
                    )
                    >= hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c2, c1],
                        confidence_level=confidence_level / 2,
                    )
                    or hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c1, c2], confidence_level=confidence_level
                    )
                    == 0
                )

        for c1, c2, c3 in zip(column1, column2, column3):
            assert hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2, c3], confidence_level=confidence_level
            ) == hstrat.calc_rank_of_mrca_uncertainty_among(
                [c3, c1, c2],
                confidence_level=confidence_level,
            )
            res = hstrat.calc_rank_of_mrca_uncertainty_among(
                [c1, c2, c3],
                confidence_level=confidence_level,
            )

            if res is not None:
                assert 0 <= res
                assert (
                    hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c1, c2, c3], confidence_level=confidence_level
                    )
                    >= hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c1, c2, c3],
                        confidence_level=confidence_level / 2,
                    )
                    or hstrat.calc_rank_of_mrca_uncertainty_among(
                        [c1, c2, c3], confidence_level=confidence_level
                    )
                    == 0
                )


@pytest.mark.filterwarnings("ignore:Empty or singleton population.")
def test_calc_rank_of_mrca_uncertainty_among_singleton():
    c1 = hstrat.HereditaryStratigraphicColumn(
        stratum_differentia_bit_width=1,
    )
    for __ in range(10):
        assert hstrat.calc_rank_of_mrca_uncertainty_among([c1]) is None
        c1.DepositStratum()

    c2 = hstrat.HereditaryStratigraphicColumn(
        stratum_differentia_bit_width=64,
    )
    for __ in range(10):
        assert hstrat.calc_rank_of_mrca_uncertainty_among([c1]) is None
        c2.DepositStratum()


@pytest.mark.filterwarnings("ignore:Empty or singleton population.")
def test_calc_rank_of_mrca_uncertainty_among_empty():
    assert hstrat.does_share_any_common_ancestor([]) is None


def test_calc_rank_of_mrca_uncertainty_among_generator():
    c1 = hstrat.HereditaryStratigraphicColumn(
        stratum_differentia_bit_width=1,
    )
    for __ in range(10):
        assert hstrat.calc_rank_of_mrca_uncertainty_among(
            [c1 for __ in range(10)]
        ) == hstrat.calc_rank_of_mrca_uncertainty_among(
            (c1 for __ in range(10))
        )
        c1.DepositStratum()

    c2 = hstrat.HereditaryStratigraphicColumn(
        stratum_differentia_bit_width=64,
    )
    for __ in range(10):
        assert hstrat.calc_rank_of_mrca_uncertainty_among(
            [c2 for __ in range(10)]
        ) == hstrat.calc_rank_of_mrca_uncertainty_among(
            (c2 for __ in range(10))
        )
        c2.DepositStratum()
