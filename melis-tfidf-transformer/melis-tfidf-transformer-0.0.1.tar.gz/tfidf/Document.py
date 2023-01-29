import warnings
import math
from bs4 import BeautifulSoup
import re
import string

class Document:
    '''
    A class to represent a Document.

    Attributes
    ----------
    __content: str
        Content of the document.
    words: list(str)
        List of words in the document.
    unique_words: list(str)
        List of unique words in the document.
    '''
    def __init__(self, content):
        '''
        Constructor for the Document object. 
        Sets the __content property.

                Parameters:
                        content (str): content of the document
                Raises:
                        TypeError: if content is not string or empty string
                        ValueError: if content is HTML or is not lowercased or includes urls, emails, punctuation, numbers or whitespace other than space.

        '''
        if type(content) != str or len(content) == 0:
            raise TypeError('A document object can only be created wit a non empty string.')

        #check for HTML
        if BeautifulSoup(content, "html.parser").find():
            raise ValueError('Document cannot be created because text includes HTML.')

        #check for URLs
        if len(re.findall(r'\w+://\w+\.\w+\.\w+/?[\w\.\?=#]*', content)) > 0:
            raise ValueError('Document cannot be created because text includes URL/s.')

        #check for emails
        if len(re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', content)) > 0:
            raise ValueError('Document cannot be created because text includes email address/es.')

        #check if lowercase
        if not content.islower():
            raise ValueError('Document cannot be created because text is not in lowercase.')

        #check if punctuation is removed
        if len([i for i in content if i in string.punctuation]) > 0:
            raise ValueError('Document cannot be created because text includes punctuation.')

        #check if numbers are removed
        if len([i for i in content if i.isdigit()]) > 0:
            raise ValueError('Document cannot be created because text includes numbers.')

        #check whitespace
        if len([i for i in content if i in string.whitespace and i != ' ']) > 0 or '  ' in content:
            raise ValueError('Document cannot be created because text includes whitespace other than space.')

        self.__content = content

    @property
    def content(self):
        '''The getter method for the __content variable.'''
        return self.__content

    @property
    def words(self):
        '''Calculates and returns the list of words in the document.'''
        return self.content.split()

    @property
    def unique_words(self):
        '''Calculates and returns the set of unique words in the document.'''
        return set(self.words)

    def n_gram(self, n):
        '''
        Calculates ngrams of the content of the document according to the n value.

                Parameters:
                        n (int): An integer in range 1 to len(content)-1
                Returns:
                        (str): list of ngrams of the content
                Raises:
                        TypeError: if n is not an integer
                        ValueError: if n is not in range 1 to len(content)-1
        '''
        if type(n) == int:
            if n > 0 and n < len(self.words):
                return [' '.join(self.words[i:i+n]) for i in range(0,len(self.words)-n+1)]
            else:
                raise ValueError('n should be bigger than 0 and less than length of the document.')
        else:
            raise TypeError('n should be int.')

    def __eq__(self, other):
        '''The equality function. 
        Since the only settable property is content it checks the equality between contents.'''
        return self.content == other.content

    def __hash__(self):
        '''The hash function. 
        Since the only settable property is content it hashes the content.'''
        return hash(self.content)

    def __repr__(self):
        '''The representation function.'''
        return f'Document({self.content})'