import pytest
from pandas.io.json._table_schema import convert_pandas_type_to_json_field

from chalk import Resolver
from chalk.features import Feature, FeatureSetBase, features, has_one, unwrap_feature
from chalk.parsed.json_conversions import convert_type_to_gql


def test_converting_filters():
    @features
    class InvalidFeatureClass2:
        id: int

    @features
    class InvalidFeatureClass:
        id: int

        relationship_id: int
        relationship: InvalidFeatureClass2 = has_one(
            lambda: InvalidFeatureClass.relationship == InvalidFeatureClass2.id
        )
        relationship2: InvalidFeatureClass2 = has_one(
            lambda: InvalidFeatureClass.relationship_id == InvalidFeatureClass2.id
        )

    # should fail -- referencing a has one in the filter
    with pytest.raises(AssertionError):
        convert_type_to_gql(unwrap_feature(InvalidFeatureClass.relationship))

    # should be fine
    convert_type_to_gql(unwrap_feature(InvalidFeatureClass.relationship2))

    del FeatureSetBase.registry["invalid_feature_class"]
    del FeatureSetBase.registry["invalid_feature_class2"]
