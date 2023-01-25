from sklearn.feature_extraction.text import TfidfVectorizer

class TfidfTransformer:
    """
    A class for allows to use fit,transform and fit_transform methods of TfidfVectorizer

    Attributes
    ----------
    documents: str
        string documents to fit the transformer

    Methods
    -------
    fit(documents):
        Allows the use of the fit method in TfidfVectorizer.
    transform(documents):
        Allows the use of the transform method in TfidfVectorizer.
    fit_transform(documents):
        Allows the use of the fit_transform method in TfidfVectorizer.
    get_feature_names:
        Allows the use of the get_feature_names method in TfidfVectorizer.
    """
    def __init__(self):
        self.tfidf = TfidfVectorizer()

    def fit(self, documents):
        """
        Fit the transformer to the given documents.
        
        Parameters
        ----------
        documents: str
            string documents to fit the transformer
        
        Returns
        -------
        None
        """
        self.tfidf.fit(documents)

    def transform(self, documents):
        """
        Transform a documents

        Parameters
        ----------
        documents: str
            string documents to transform
        
        Returns
        -------
        transformed documents in sparse matrix format
        """
        return self.tfidf.transform(documents)
    
    def fit_transform(self, documents):
        """
        Fit and transform the transformer to the given string documents
        
        Parameters
        ----------
        documents: str
            string documents to fit and transform
        
        Returns
        -------
        transformed documents in parsing matrix format
        """
        return self.tfidf.fit_transform(documents)
    
    def get_feature_names(self):
        """
        Returns the feature names
        """
        return self.tfidf.get_feature_names()