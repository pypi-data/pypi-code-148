import dataclasses
import json

from chalk.features import features, sink
from chalk.parsed.duplicate_input_gql import UpsertSinkResolverGQL
from chalk.parsed.json_conversions import convert_type_to_gql


@features
class SinkFeatures:
    scalar_feature: str


@sink(debounce="2s", max_delay="10s")
def sink_fn(f: SinkFeatures.scalar_feature):
    return f


def test_callable():
    assert sink_fn("4") == "4"
    converted = convert_type_to_gql(sink_fn)
    assert isinstance(converted, UpsertSinkResolverGQL)
    json.dumps(dataclasses.asdict(converted))
