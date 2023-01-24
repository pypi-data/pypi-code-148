import unittest

import pandasdmx
import pandas as pd

from fso_metadata.constants import BASE_URL
from fso_metadata.format_request import sdmx_request, dict_to_string
from test.test_constants import TEST_CODELIST_ID


class TestSdmxRequest(unittest.TestCase):
    def test_sdmx_request(self):
        url = f'{BASE_URL}/api/Codelists/{TEST_CODELIST_ID}/exports/SDMX-ML/2.1'
        params_possible = ['true', 'false']
        for params in params_possible:
            params_string = f'annotations={params}'
            res = sdmx_request(url, params_string)
            assert type(res) == pandasdmx.util.DictLike, 'Wrong output type'

            
class TestDictToString(unittest.TestCase):
    def test_dict_to_string(self):
        self.assertEqual(dict_to_string(
            {'a': [1, 2], 'b': [3]}
        ), 'a=1&a=2&b=3')
        self.assertEqual(dict_to_string(
            {'a': ['testing'], 'b': ['the'], 'c': [], 'd': ['code']}
        ), 'a=testing&b=the&d=code')
        self.assertEqual(dict_to_string(
            {'AF_ACTIVE': [1], 'AF_AVAM': [1]}
        ), 'AF_ACTIVE=1&AF_AVAM=1')
