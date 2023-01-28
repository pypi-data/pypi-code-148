import pytest
from pydantic import BaseModel

from chalk.features import DataFrame, features
from chalk.features.resolver import StreamResolver
from chalk.sql._internal.sql_file_resolver import SQLStringResult, get_sql_file_resolver
from chalk.streams import KafkaSource, Windowed, stream, windowed

try:
    import duckdb
except ImportError:
    duckdb = None


try:
    import polars as pl
except ImportError:
    pl = None


@features
class StoreFeatures:
    id: str
    purchases: Windowed[float] = windowed("10m", "20m")


class KafkaMessage(BaseModel):
    purchase_id: str
    store_id: str
    amount: float


source = KafkaSource(bootstrap_server="server", topic="topic", name="kafka_test_source")


@stream(source=source)
def fn(messages: DataFrame[KafkaMessage]) -> DataFrame[StoreFeatures.id, StoreFeatures.purchases]:
    return f"""
        select store_id as id, sum(amount) as purchases
        from {messages}
        group by 1
    """


@pytest.mark.skipif(duckdb is None or pl is None, reason="duckdb is not installed or polars is not installed")
def test_runs_sql():
    assert pl is not None
    expected = DataFrame(
        pl.DataFrame(
            {
                "store_features.id": ["store1", "store2"],
                "store_features.purchases": [10, 5],
            },
        )
    )
    actual = fn(
        DataFrame(
            pl.DataFrame(
                {
                    "store_id": ["store1", "store2", "store1"],
                    "amount": [4, 5, 6],
                }
            ),
            pydantic_model=KafkaMessage,
        )
    )

    # polars.testing.assert_frame_equal(actual, expected)
    assert expected.to_pyarrow() == actual.to_pyarrow()


@pytest.mark.skipif(duckdb is None or pl is None, reason="duckdb is not installed or polars is not installed")
def test_sql_file_stream_resolver():
    sources = [source]
    sql_string = """-- source: kafka_test_source
        -- resolves: store_features
        -- type: streaming
        select store_id as id, sum(amount) as purchases
        from topic
        group by 1
    """
    sql_string_result = SQLStringResult(path="sample_path", sql_string=sql_string, error=None)
    resolver_result = get_sql_file_resolver(sources, sql_string_result)
    assert not resolver_result.errors
    assert resolver_result.fields == {"id": "store_features.id", "purchases": "store_features.purchases"}
    res = resolver_result.resolver
    assert (
        res.sql_query
        == """select store_id as id, sum(amount) as purchases
        from topic
        group by 1"""
    )
    assert res.source == source


@pytest.mark.skipif(duckdb is None or pl is None, reason="duckdb is not installed or polars is not installed")
def test_sql_file_stream_resolver_kafka():
    sources = [source]
    sql_string = """-- source: kafka
        -- resolves: store_features
        -- type: streaming
        select store_id as id, sum(amount) as purchases
        from topic
        group by 1
    """
    sql_string_result = SQLStringResult(path="sample_path", sql_string=sql_string, error=None)
    resolver_result = get_sql_file_resolver(sources, sql_string_result)
    assert not resolver_result.errors
    assert resolver_result.fields == {"id": "store_features.id", "purchases": "store_features.purchases"}
    res = resolver_result.resolver
    assert isinstance(res, StreamResolver)
    assert (
        res.sql_query
        == """select store_id as id, sum(amount) as purchases
        from topic
        group by 1"""
    )
