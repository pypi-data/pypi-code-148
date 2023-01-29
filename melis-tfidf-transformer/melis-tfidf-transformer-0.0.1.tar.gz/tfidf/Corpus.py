from .Document import Document
import math
import warnings
import numpy as np

class Corpus:
    '''
    A class to represent a collection of Document objects.

    Attributes
    ----------
    __documents: tuple(Document)
        Document objects in the corpus
    n_documents: int
        Number of Document objects in the corpus
    '''
    def __init__(self, docs):
        '''
        Constructor for the Corpus object. 
        Calls the setter method for the __documents property.

                Parameters:
                        docs (list(Document)): List of Document object/s.
        '''
        self.documents = docs

    @property
    def documents(self):
        '''The getter method for the __documents variable.'''
        return self.__documents

    @documents.setter
    def documents(self, docs):
        '''
        Sets the documents of the corpus to the given list of documents. Ignores duplicates.

                Parameters:
                        docs (list(Document)): List of Document object/s.
                Raises:
                        TypeError: if docs is not a list of Document object/s.
                Warns:
                        UserWarning: if there duplicate documents.
        '''
        if type(docs) == list and len(docs) > 0 and all(isinstance(x, Document) for x in docs):
            self.__documents = tuple(set(docs))
            if self.n_documents != len(docs):
                warnings.warn('Unable to add duplicate document/s.')
        else:
            raise TypeError('Corpus documents can only be set with a list of Document object/s.')

    def add_documents(self, docs):
        '''
        Adds the documents in the given Document list to the corpus.

                Parameters:
                        docs (list(Document)): List of Document object/s.
                Raises:
                        TypeError: if docs is not a list of Document object/s.
        '''
        if type(docs) == list and len(docs) > 0 and all(isinstance(x, Document) for x in docs):
            self.documents = list(self.documents) + docs
        else:
            raise TypeError('Only a list of Document object/s can be added to the corpus.')

    def remove_documents(self, docs):
        '''
        Removes the documents in the given Document list from the corpus.

                Parameters:
                        docs (list(Document)): List of Document object/s.
                Raises:
                        TypeError: if docs is not a list of Document object/s.
                        ValueError: if removing docs results in removing all of the Documents in the corpus.
        '''
        if type(docs) == list and len(docs) > 0 and all(isinstance(x, Document) for x in docs):
            idxs = list()
            for d in docs:
                try:
                    idxs.append(self.documents.index(d))
                except ValueError:
                    warnings.warn('Document cannot be removed because it is not present in corpus.')
                finally:
                    continue

            updated_docs = [d for i,d in enumerate(self.documents) if i not in idxs]
            if len(updated_docs) > 0:
                self.documents = updated_docs
            else:
                raise ValueError('Remove cannot be done because it will remove all of the documents in the corpus.')
        else:
            raise TypeError('Only a list of Document object/s can be removed from the corpus.')

    @property
    def n_documents(self):
        '''Calculates and return the number of documents in the corpus.'''
        return len(self.documents)

    def exists(self, docs):
        '''
        Calculates and returns truth values for whether the document exists in the corpus.

                Parameters:
                        docs (list(Document)): List of Document object/s.
                Returns:
                        (list(Boolean)): list of truth values denoting whether the document exists
                Raises:
                        TypeError: if docs is not a list of Document object/s.
        '''
        if type(docs) == list and len(docs) > 0 and all(isinstance(x, Document) for x in docs):
            return [d in self.documents for d in docs]
        else:
            raise TypeError('Only a list of Document object/s can be checked.')

    def __idf(self, seq, n):
        '''
        Calculates and returns the idf value for the given sequence according to the documents in the corpus.
        In order to eliminate division-by-zero errors for sequences not present in corpus the formula is adjusted into 
        log(total number of documents in the corpus/(1 + number of documents where sequence appears)).

                Parameters:
                        seq (str): An ngram.
                        n (int): An integer in range 1 to len(content)-1
                Returns:
                        (float): IDF value for the given sequence according to the documents in the corpus
        '''
        d_count = 1
        for d in self.documents:
            if seq in d.n_gram(n):
                d_count += 1

        return math.log(self.n_documents/d_count)

    def __unique_ngrams(self, docs, n):
        '''
        Calculates and returns unique ngrams present in the corpus and the given document list.

                Parameters:
                        docs (list(Document)): List of Document object/s
                        n (int): An integer in range 1 to len(content)-1
                Returns:
                        (str): list of unique ngrams of the content
        '''
        unique_ngrams = set()
        for d in self.documents:
            unique_ngrams.update(d.n_gram(n))
        for d in docs:
            unique_ngrams.update(d.n_gram(n))
        return list(unique_ngrams)

    def tf_idf(self, docs, n):
        '''
        Calculates and returns tfidf values for the given list of documents.

                Parameters:
                        docs (list(Document)): List of Document object/s
                        n (int): An integer in range 1 to min len(content)-1 for the Documents in the corpus and docs
                Returns:
                        tf_idfs (list(np.array)): list of tfidf values for the unique ngrams in the corpus and docs
                        unique_ngrams (list(str)): list of unique ngrams in the corpus and docs
                Raises:
                        TypeError: if docs is not a list of Document object/s.
                        ValueError: if n is not an int, n < 1, n > min len(content)-1 for the Documents in the corpus and docs

        '''
        if type(docs) == list and len(docs) > 0 and all(isinstance(x, Document) for x in docs):
            min_n = min(min([len(d.words) for d in self.documents]), min([len(d.words) for d in docs]))
            if type(n) == int and n > 0 and n < min_n:
                unique_ngrams = self.__unique_ngrams(docs, n)
                tf_idfs = list()
                idfs = dict()
                for d in docs:
                    tfidf = np.zeros(len(unique_ngrams))
                    ngram_list = d.n_gram(n)
                    for item in ngram_list:
                        tf = ngram_list.count(item)/len(ngram_list)
                        if item not in idfs:
                            idfs[item] = self.__idf(item, n)
                        tfidf[unique_ngrams.index(item)] = tf*idfs[item]
                    tf_idfs.append(tfidf)

                return tf_idfs, unique_ngrams
            else:
                raise ValueError('n value should be int, should be bigger than 0 and less than the length of the shortest document in corpus and given documents.')
        else:
            raise TypeError('Tf-idf values can only be calculated for a list of Document objects.')

    def __repr__(self):
        '''The representation function.'''
        return f'Corpus({self.documents})'