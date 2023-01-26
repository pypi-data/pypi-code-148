import unittest
import json
from pathlib import Path

from custom_json_encoder import CustomJSONEncoder


def stringify(obj):
    if isinstance(obj, Path):
        return obj.as_posix()
    return str(obj)


class TestCustomJSONEncoder(unittest.TestCase):

    def test_1(self):
        data = {
            "a": 1,
            "b": 2,
            "c": 3,
        }
        expected = """{
    "a": 1,
    "b": 2,
    "c": 3
}"""
        self.assertEqual(json.dumps(data, indent=4, cls=CustomJSONEncoder), expected)
    
    def test_2(self):
        data = {Path("."): "a"}
        expected = """{
    ".": "a"
}"""
        self.assertEqual(json.dumps(data, default=stringify, indent=4, cls=CustomJSONEncoder), expected)
    
    def test_3(self):
        data = {"a": Path("."),}
        expected = """{
    "a": "."
}"""
        self.assertEqual(json.dumps(data, default=stringify, indent=4, cls=CustomJSONEncoder), expected)
