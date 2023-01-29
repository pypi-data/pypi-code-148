import pytest
from ...src.parser.YAML_parser import YAMLParser

# Test data
valid_yaml = """
dag:
  id: my_dag
  data_path: /path/to/data
  output_folder: /path/to/output
  description: My DAG
  feature_engineering: feature_engineering.py
  model: my_model.py
"""

invalid_yaml = """
dag:
  data_path: /path/to/data
  output_folder: /path/to/output
  description: My DAG
  feature_engineering: feature_engineering.py
  model: my_model.py
"""

expected_output = {
    "dag_id": "my_dag",
    "data_path": "/path/to/data",
    "output_folder": "/path/to/output",
    "description": "My DAG",
    "feature_engineering": "feature_engineering.py",
    "model": "my_model.py",
}


# Fixtures
@pytest.fixture
def valid_yaml_parser():
    with open("valid_config.yaml", "w") as f:
        f.write(valid_yaml)
    return YAMLParser("valid_config.yaml")


@pytest.fixture
def invalid_yaml_parser():
    with open("invalid_config.yaml", "w") as f:
        f.write(invalid_yaml)
    return YAMLParser("invalid_config.yaml")


# Tests
def test_valid_yaml(valid_yaml_parser):
    assert valid_yaml_parser.parse() == expected_output


def test_invalid_yaml(invalid_yaml_parser):
    with pytest.raises(ValueError, match=r".*Error in file invalid_config.yaml: the field `id` is required.*"):
        invalid_yaml_parser.parse()
