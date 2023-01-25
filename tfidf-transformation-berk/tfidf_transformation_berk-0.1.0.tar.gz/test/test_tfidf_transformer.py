import unittest
from tfidf_transformation_brk import TfidfTransformer

class TestTfidfTransformer(unittest.TestCase):
    def setUp(self):
        self.transformer = TfidfTransformer()
        self.documents = ['A Scandal in Bohemia', 'The Red-headed League', 'A Case of Identity', 'The Boscombe Valley Mystery', 'The Five Orange Pips', 'The Man with the Twisted Lip', 'The Adventure of the Blue Carbuncle', 'The Adventure of the Speckled Band', 'The Adventure of the Noble Bachelor']

    def test_fit(self):
        self.transformer.fit(self.documents)
        self.assertIsNotNone(self.transformer.tfidf)
    
    def test_fit_invalid_input(self):
        with self.assertRaises(ValueError):
            self.transformer.fit(None)
    
    def test_transform(self):
        self.transformer.fit(self.documents)
        transform = self.transformer.transform(self.documents)
        self.assertIsInstance(transform)
    
    def test_transform_invalid_input(self):
        with self.assertRaises(ValueError):
            self.transformer.transform(None)
        
    def test_fit_transform(self):
        fit_transform = self.transformer.fit_transform(self.documents)
        self.assertIsInstance(fit_transform)

    def test_fit_transform_invalid_input(self):
        with self.assertRaises(ValueError):
            self.transformer.fit_transform(None)
        
    def test_get_feature_names(self):
        self.transformer.fit(self.documents)
        feature_names = self.transformer.get_feature_names()
        self.assertIsInstance(feature_names,list)

if __name__ == '__main__':
    unittest.main()