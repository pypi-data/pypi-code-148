try:
    import polars as pl
except ImportError:
    pl = None

from datetime import datetime

import pytest

from chalk.client.dataset import DatasetVersion, _extract_df_columns
from chalk.features import feature, feature_time, features, has_one


@features
class Transaction:
    id: int = feature(primary=True)
    user_id: int
    amount: float
    ts: datetime = feature_time()


@features
class TransactionPointer:
    id: int = feature(primary=True)
    transaction_id: int = feature(max_staleness="infinity")
    transaction: Transaction = has_one(lambda: Transaction.id == TransactionPointer.transaction_id)


@pytest.mark.skipif(pl is None, reason="Polars is not installed")
def test_feature_explosion_load_dataset():
    schema = [
        "__id__",
        "__oat__",
        "__rat__",
        "__ts__",
        "cb_orzgc3ttmfrxi2lpnyxgc3lpovxhi000",
        "cb_orzgc3ttmfrxi2lpnyxgc3lpovxhils7l5xwc5c7l4000000",
        "cb_orzgc3ttmfrxi2lpnyxgc3lpovxhils7l5zgc5c7l4000000",
        "cb_orzgc3ttmfrxi2lpnyxgsza0",
        "cb_orzgc3ttmfrxi2lpnyxgszbol5pw6ylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnyxgszbol5pxeylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnyxhi4y0",
        "cb_orzgc3ttmfrxi2lpnyxhk43fojpwsza0",
        "cb_orzgc3ttmfrxi2lpnyxhk43fojpwszbol5pw6ylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnyxhk43fojpwszbol5pxeylul5pq0000",
    ]
    data = [None] * len(schema)
    df = pl.DataFrame([data], columns=schema)
    result = _extract_df_columns(
        df=df,
        output_feature_fqns=["transaction"],
        output_ts=False,
        output_id=False,
        version=DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
    )
    assert result.columns == ["transaction.amount", "transaction.id", "transaction.ts", "transaction.user_id"]

    schema = [
        "__id__",
        "__oat__",
        "__rat__",
        "__ts__",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4rol5pwg2dbnrvv633consxe5tfmrpwc5c7l4000000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4ronfsa0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4ronfsc4x27n5qxix27",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4ronfsc4x27ojqxix27",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgc3lpovxhi000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgc3lpovxhils7l5xwc5c7l4000000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgc3lpovxhils7l5zgc5c7l4000000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgsza0",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgszbol5pw6ylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxgszbol5pxeylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxhk43fojpwsza0",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxhk43fojpwszbol5pw6ylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnyxhk43fojpwszbol5pxeylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnzpwsza0",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnzpwszbol5pw6ylul5pq0000",
        "cb_orzgc3ttmfrxi2lpnzpxa33jnz2gk4roorzgc3ttmfrxi2lpnzpwszbol5pxeylul5pq0000",
    ]
    data = [None] * len(schema)
    df = pl.DataFrame([data], columns=schema)
    result = _extract_df_columns(
        df=df,
        output_feature_fqns=["transaction_pointer.transaction"],
        output_ts=False,
        output_id=False,
        version=DatasetVersion.BIGQUERY_JOB_WITH_B32_ENCODED_COLNAMES,
    )
    assert result.columns == [
        "transaction_pointer.transaction.amount",
        "transaction_pointer.transaction.id",
        "transaction_pointer.transaction.user_id",
    ]
