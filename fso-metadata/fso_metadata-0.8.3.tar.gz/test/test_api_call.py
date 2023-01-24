import unittest

import pandas as pd

from fso_metadata.api_call import (
    get_codelist, 
    get_data_structure, 
    get_nomenclature_one_level, 
    get_nomenclature_multiple_levels
)
from test.test_constants import TEST_CODELIST_ID, TEST_DATASTRUCTURE_ID, TEST_NOMENCLATURE_ID


class TestGetCodelist(unittest.TestCase):
    def test_get_codelist(self):
        res = get_codelist(identifier=TEST_CODELIST_ID, export_format="SDMX-ML")
        assert type(res) == pd.core.series.Series, 'Wrong codelist output type'
        

class TestGetDataStructure(unittest.TestCase):
    def test_get_data_structure(self):
        res = get_data_structure(identifier=TEST_DATASTRUCTURE_ID, language="fr")
        assert type(res) == dict, 'Wrong data structure output type'

        
class TestNomOneLevel(unittest.TestCase):
    def test_get_nomenclature_one_level(self):
        res = get_nomenclature_one_level(
            identifier=TEST_NOMENCLATURE_ID, 
            level_number=2, 
            language='en'
        )
        assert type(res) == pd.core.frame.DataFrame, 'Wrong data structure output type'
        self.assertListEqual(list(res.columns), [
            'Code', 
            'Parent', 
            'Name_en'
        ])


class TestNomMultipleLevels(unittest.TestCase):
    def test_get_nomenclature_multiple_levels(self):
        res = get_nomenclature_multiple_levels(
            identifier=TEST_NOMENCLATURE_ID, 
            level_from=1, 
            level_to=6, 
            language='en'
        )
        
        assert type(res) == pd.core.frame.DataFrame, 'Wrong data structure output type'
        self.assertListEqual(list(res.columns), [
            'Major_groups', 
            'Sub-major_groups', 
            'Minor_groups', 
            'Unit_groups', 
            'Type', 
            'Occupations', 
            'Code', 
            'Name_en'
        ])
