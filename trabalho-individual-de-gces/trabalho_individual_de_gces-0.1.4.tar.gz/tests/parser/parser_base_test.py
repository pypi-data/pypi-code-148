import pytest
from ...src.parser.parser_base import ParserBase


@pytest.fixture
def parser():
    return ParserBase()


@pytest.mark.parametrize("variable, field, expected_output", [
    ({'field1': 'value1'}, 'field1', 'value1'),
    ({'field1': 'value1'}, 'field2', ValueError),
    ({'field1': 'value1'}, 'value2', ValueError)
])
def test_try_get(parser, variable, field, expected_output):
    if expected_output == KeyError:
        with pytest.raises(KeyError):
            parser._try_get(variable, field)
    elif expected_output == ValueError:
        with pytest.raises(ValueError):
            parser._try_get(variable, field)
    else:
        assert parser._try_get(variable, field) == expected_output


@pytest.mark.parametrize("variable, field, default_value, expected_output", [
    ({'field1': 'value1'}, 'field1', 'default', 'value1'),
    ({'field1': 'value1'}, 'field2', 'default', 'default')
])
def test_get(parser, variable, field, default_value, expected_output):
    assert parser._get(variable, field, default_value) == expected_output
