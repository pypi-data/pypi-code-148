import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List
import scipy


class TfIdfTransformer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, documents: List[str]) -> scipy.sparse.csr_matrix:
        """
        Fit the Tf-Idf model on the input documents and returns the transformed matrix.
        Handle edge cases of empty or None input.
        """
        if not documents or not all(documents):
            raise ValueError("Input documents cannot be empty or None.")
        return self.vectorizer.fit_transform(documents)

    def transform(self, documents: List[str]) -> scipy.sparse.csr_matrix:
        """
        Transforms the input documents using the previously fitted Tf-Idf model.
        Handle edge cases of empty or None input.
        """
        if not documents or not all(documents):
            raise ValueError("Input documents cannot be empty or None.")
        return self.vectorizer.transform(documents)