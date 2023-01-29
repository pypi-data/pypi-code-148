from pynalytics.parser.parser_base import ParserBase

import pytest

def test_try_get():
    parser = ParserBase()
    variable = {'field': 'value'}
    assert parser._try_get(variable, 'field') == 'value'
    with pytest.raises(ValueError) as e:
        parser._try_get(variable, 'missing_field')
    assert str(e.value) == 'Error in file config.yaml: the field `missing_field` is required.'