
import pandas as pd
import pytest
from ....src.data_pipeline.pre_processing.concatenate_columns import get_concatenated_column
# Test cases that should pass
passing_test_cases = [
    {'csv': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}), 'columns': 'col1', 'column_name': 'new_col',
     'expected': pd.DataFrame({'new_col': [1, 2, 3]})},
    {'csv': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6], 'col3': [7, 8, 9]}), 'columns': ['col1', 'col2'],
     'column_name': 'new_col', 'expected': pd.DataFrame({'new_col': ['1 4', '2 5', '3 6']})},
]

# Test cases that should fail
failing_test_cases = [
    {'csv': pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}), 'columns': ['col1', 'col3'], 'column_name': 'new_col',
     'expected': KeyError},
]


@pytest.mark.parametrize("test_case", passing_test_cases)
def test_get_concatenated_column_passes(test_case):
    csv = test_case['csv']
    columns = test_case['columns']
    column_name = test_case['column_name']
    expected = test_case['expected']

    result = get_concatenated_column(csv, columns, column_name)
    assert result.equals(expected)


@pytest.mark.parametrize("test_case", failing_test_cases)
def test_get_concatenated_column_fails(test_case):
    csv = test_case['csv']
    columns = test_case['columns']
    column_name = test_case['column_name']
    expected = test_case['expected']

    with pytest.raises(expected):
        get_concatenated_column(csv, columns, column_name)
