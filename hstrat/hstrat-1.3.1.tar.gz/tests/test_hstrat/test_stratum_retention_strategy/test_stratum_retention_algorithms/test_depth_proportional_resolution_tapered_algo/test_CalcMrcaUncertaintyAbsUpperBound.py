import numpy as np
import pytest

from hstrat.hstrat import depth_proportional_resolution_tapered_algo


@pytest.mark.parametrize(
    "depth_proportional_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
@pytest.mark.parametrize(
    "time_sequence",
    [
        range(10**3),
        (i for i in range(10**2) for __ in range(2)),
        np.random.default_rng(1).integers(
            low=0,
            high=2**32,
            size=10**2,
        ),
        (2**32,),
    ],
)
def test_policy_consistency(depth_proportional_resolution, time_sequence):
    policy = depth_proportional_resolution_tapered_algo.Policy(
        depth_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = depth_proportional_resolution_tapered_algo.CalcMrcaUncertaintyAbsUpperBound(
        spec,
    )
    for num_strata_deposited in time_sequence:
        for actual_mrca_rank in (
            np.random.default_rng(num_strata_deposited,).integers(
                low=0,
                high=num_strata_deposited,
                size=10**2,
            )
            if num_strata_deposited
            else iter(())
        ):
            policy_requirement = policy.CalcMrcaUncertaintyAbsExact(
                num_strata_deposited,
                num_strata_deposited,
                actual_mrca_rank,
            )
            for which in (
                instance,
                depth_proportional_resolution_tapered_algo.CalcMrcaUncertaintyAbsUpperBound(
                    spec
                ),
            ):
                assert (
                    which(
                        policy,
                        num_strata_deposited,
                        num_strata_deposited,
                        actual_mrca_rank,
                    )
                    >= policy_requirement
                )


@pytest.mark.parametrize(
    "depth_proportional_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_eq(depth_proportional_resolution):
    policy = depth_proportional_resolution_tapered_algo.Policy(
        depth_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = depth_proportional_resolution_tapered_algo.CalcMrcaUncertaintyAbsUpperBound(
        spec
    )

    assert instance == instance
    assert (
        instance
        == depth_proportional_resolution_tapered_algo.CalcMrcaUncertaintyAbsUpperBound(
            spec,
        )
    )
    assert instance is not None


@pytest.mark.parametrize(
    "depth_proportional_resolution",
    [
        1,
        2,
        3,
        7,
        42,
        97,
        100,
    ],
)
def test_negative_index(depth_proportional_resolution):
    policy = depth_proportional_resolution_tapered_algo.Policy(
        depth_proportional_resolution
    )
    spec = policy.GetSpec()
    instance = depth_proportional_resolution_tapered_algo.CalcMrcaUncertaintyAbsUpperBound(
        spec
    )

    for diff in range(1, 100):
        assert instance(policy, 100, 100, -diff,) == instance(
            policy,
            100,
            100,
            99 - diff,
        )

        assert instance(policy, 101, 100, -diff,) == instance(
            policy,
            101,
            100,
            99 - diff,
        )

        assert instance(policy, 150, 100, -diff,) == instance(
            policy,
            150,
            100,
            99 - diff,
        )

        assert instance(policy, 100, 101, -diff,) == instance(
            policy,
            101,
            100,
            99 - diff,
        )

        assert instance(policy, 100, 150, -diff,) == instance(
            policy,
            150,
            100,
            99 - diff,
        )
