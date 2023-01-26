#!/usr/bin/env python3

import unittest

import json

# importing library functions
from imcs.lib.verify_functions import load_json_file

class IMCS_Testsuite(unittest.TestCase):
    def test_valid_json(self):
        json = {
                "@context": "http://schema.org",
                "@id": "own URL",
                "@type": "Dataset",
                "dct:conformsTo": "https://bioschemas.org/profiles/Dataset/0.3-RELEASE-2019_06_14",
                "description": "my description",
                "identifier": [
                    "my identifier for item 1",
                    "my identifier for item 1"
                    ],
                "keywords": [
                "my keywords"
                    ],
                "name": "my name",
                "url": "own download URL - may be same as in @id"
                }
        self.assertEqual(load_json_file('imcs/sample_data/schema_plain.json'),
                json)

    def test_errornous_json(self):
        with self.assertRaises(json.decoder.JSONDecodeError):
            load_json_file('imcs/sample_data/schema_erroneous.json')

if __name__ == '__main__':
    unittest.main()
