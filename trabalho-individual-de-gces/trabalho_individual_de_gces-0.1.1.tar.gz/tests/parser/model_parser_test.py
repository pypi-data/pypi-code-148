import pytest
from ...src.parser.model_parser import ModelParser


@pytest.mark.parametrize(
    "data, expected_output",
    [
        (
            {
                "random_forest": [
                    {
                        "input": {
                            "type": "ADDRESS",
                            "columns": ["col1", "col2"],
                            "thresholds": {"test_size": 0.2, "n_estimators": 50},
                        }
                    }
                ]
            },
            [],
        ),
        (
            {
                "random_forest": [
                    {
                        "input": {
                            "type": "ADDRESS",
                            "columns": ["col1", "col2"],
                            "thresholds": {
                                "test_size": 0.2,
                                "n_estimators": 50,
                                "keyboard_smash": {"col1": 1.00, "col2": 2.2499},
                            },
                        }
                    }
                ]
            },
            [],
        ),
    ],
)
def test_parse(data, expected_output):
    columns_alias = ["col1", "col2"]
    parser = ModelParser(columns_alias)
    assert parser.parse(data) == expected_output
