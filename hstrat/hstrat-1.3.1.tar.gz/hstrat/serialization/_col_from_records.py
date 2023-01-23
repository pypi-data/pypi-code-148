import itertools as it
import typing

from .._auxiliary_lib import get_hstrat_version, log_once_in_a_row
from ..genome_instrumentation import (
    HereditaryStratigraphicColumn,
    HereditaryStratumOrderedStoreList,
)
from ._unpack_differentiae import unpack_differentiae


def col_from_records(records: typing.Dict) -> HereditaryStratigraphicColumn:
    """Deserialize a `HereditaryStratigraphicColumn` from a dict composed of
    builtin data types.
    """
    if "deposition_ranks" in records or "stratum_annotations" in records:
        raise NotImplementedError

    if get_hstrat_version() != records["hstrat_version"]:
        log_once_in_a_row(
            f"""col_from_records version mismatch, record is version {
                records['hstrat_version']
            } and software is version {
                get_hstrat_version()
            }"""
        )

    def load_policy():
        # noqa
        from ..stratum_retention_strategy import (
            stratum_retention_algorithms as hstrat,
        )

        return eval(records["policy"])  # noqa

    def load_stratum_ordered_store() -> HereditaryStratumOrderedStoreList:
        dummy_column = HereditaryStratigraphicColumn(
            stratum_retention_policy=load_policy(),
            stratum_differentia_bit_width=records["differentia_bit_width"],
        )
        store = HereditaryStratumOrderedStoreList()

        for differentia, deposition_rank, annotation in zip(
            unpack_differentiae(
                records["differentiae"],
                differentia_bit_width=records["differentia_bit_width"],
            ),
            records.get("stratum_deposition_ranks", it.repeat(None)),
            records.get("stratum_annotation", it.repeat(None)),
        ):
            store.DepositStratum(
                rank=deposition_rank,
                stratum=dummy_column._CreateStratum(
                    annotation=annotation,
                    differentia=differentia,
                    deposition_rank=deposition_rank,
                ),
            )
        return store

    return HereditaryStratigraphicColumn(
        stratum_retention_policy=load_policy(),
        stratum_differentia_bit_width=records["differentia_bit_width"],
        stratum_ordered_store=(
            load_stratum_ordered_store(),
            records["num_strata_deposited"],
        ),
    )
