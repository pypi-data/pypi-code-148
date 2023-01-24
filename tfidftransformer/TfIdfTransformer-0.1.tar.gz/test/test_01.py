
import unittest
from src.TfIdfTransformer import TfIdfTransformer


class TestTfIdfTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TfIdfTransformer()
        self.documents = [
            "This is the first document.",
            "This document is the second document.",
            "And this is the third one.",
            "Is this the first document?",
        ]

    def test_fit_transform(self):
        matrix = self.transformer.fit_transform(self.documents)
        self.assertEqual(matrix.shape, (4, 9)) # 4 documents and 9 unique terms

    def test_transform(self):
        self.transformer.fit_transform(self.documents) # fit the model first
        matrix = self.transformer.transform(self.documents)
        self.assertEqual(matrix.shape, (4, 9)) # 4 documents and 9 unique terms

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            self.transformer.fit_transform([])
        with self.assertRaises(ValueError):
            self.transformer.transform([])

    def test_none_input(self):
        with self.assertRaises(ValueError):
            self.transformer.fit_transform(None)
        with self.assertRaises(ValueError):
            self.transformer.transform(None)