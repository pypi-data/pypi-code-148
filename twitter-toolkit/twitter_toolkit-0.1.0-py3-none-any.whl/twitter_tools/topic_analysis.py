import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import stanza
from gensim import corpora
from gensim.models.ldamodel import LdaModel
import demoji
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

import logging

from tqdm import tqdm

logger = logging.getLogger(__name__)
supported_lang = {'es':'spanish','en':'english', 'pt':'portuguese'}

class TopicAnalysis:

    def __init__(self, language, logging_level = logging.INFO):

        if language not in supported_lang.keys():
            logging.error('Error! language not accepted. Accepted languages:'+str(list(supported_lang.keys())))
            raise Exception('Unsupported language for TopicAnalysis')

        logging.basicConfig(level=logging_level)
        self.language = language
        self.stop_words = set(stopwords.words(supported_lang[language]))
        self.nlp = stanza.Pipeline(lang=language, processors='tokenize,mwt,pos,lemma')
        self.sent_pipeline = None

    def sentiment_analysis(self, doc):
        """
        Sentiment analysis for text.

        Parameters
        ----------
        doc : String
            Doc to have a sentiment analysis on.
        
        Returns
        -------
        Dict
            Of the sentiment tag (POS, NEU, NEG) with the highest score 
            with the sentiment ('label') and the score ('score').
            E.g. : {'label': 'NEG', 'score': 0.9960648417472839}

        """

        if self.sent_pipeline == None:
            if self.language == 'es':
                sent_token = AutoTokenizer.from_pretrained("pysentimiento/robertuito-sentiment-analysis")
                sent_model = AutoModelForSequenceClassification.from_pretrained("pysentimiento/robertuito-sentiment-analysis")
                self.sent_pipeline = pipeline("sentiment-analysis", model=sent_model, tokenizer=sent_token)
            elif self.language == 'en':
                self.sent_pipeline = pipeline("sentiment-analysis",model="siebert/sentiment-roberta-large-english")
            # elif self.language == 'pt': # Portuguese model not available yet
            else:
                logging.error('Error! language not accepted. Accepted languages:es,en')
                raise Exception('Unsupported language for SentimentAnalysis')
        
        return self.sent_pipeline(doc)[0]
    
    def clean_docs(self, docs, tweet_users_hashtags=True, urls=True, stop_words=False,
                    punctuation=False, emojis=True, specific_words=[]):
        """
        Clean documents from unwanted parts.
        Thought to be used for tweets.

        Parameters
        ----------
        docs : List of Strings
            Docs to be cleaned. 
            If only one doc to be cleaned use a one element list.
        tweet_users_hashtags: Boolean
            Whether to clean users and hashtags.
            Words preceded by a '#' or a '@'
        urls: Boolean
            Whether to clean urls
            Basically strings starting with 'http'
        stop_words: Boolean
            Whether to remove stopwords.
            When removing stop words, docs returned will be lower cased
            Default is False, useful for lemmatizing and POStagging
        punctuation: Boolean
            Whether to remove punctuation.
            Default is False, useful for lemmatizing and POStagging
        emojis: Boolean
            Whether to remove emojis from text.
        specific_words: List of Strings
            remove some specific words, like the ones used for to query the docs
        
        Returns
        -------
        list
            A list of documents 'cleaned'
        """
        
        if tweet_users_hashtags:
            # remove hashtags and mention to users
            docs = [re.sub(r'[@#]\w+', ' ',doc) for doc in docs]

        if urls:
            docs = [re.sub(r'\bhttps?://[^\s]*',' ', doc) for doc in docs]
        
        if stop_words:
            tokenised = [word_tokenize(doc.lower()) for doc in docs]
            tokens_wo_stopwords = [[t for t in toks if t not in self.stop_words] for toks in tokenised]
            docs = [' '.join(tokens) for tokens in tokens_wo_stopwords]

        if punctuation:
            docs = [doc.translate(str.maketrans('', '', string.punctuation)) for doc in docs]

        if emojis:
            docs = [demoji.replace(doc, "") for doc in docs]
        
        for w in specific_words:
            docs = [doc.replace(w, "") for doc in docs]
        
        return docs


    def lemmatize(self, docs, filter_postags = False, verbose=True):
        """
        Transform documents into a list of lemmatized words.
        You can also select the POSTAGS to filter.

        Parameters
        ----------
        docs: List of Srtrings
            The documents to lemmatize.
            If only one doc to be cleaned use a one element list.
        filter_postags: `False` or List of TAGS
            False to avoid any filtering, or a list of tags to keep words.
            The available tags are ADJ, ADP, ADV, AUX, CCONJ, DET, INTJ, NOUN,
            NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB, X.
            For more info: https://universaldependencies.org/u/pos/
        verbose: Boolean
            Whether to diplay a progressbar for the lemmatization process

        Returns
        -------
        list
            A list of a list of lemmas.
            example: ["Yo comí una manzana"] -> [["yo", "comer", "una", "manzana"]]
        """
        if verbose:
            iter_docs = tqdm(docs)
        else:
            iter_docs = docs

        doc_nlps = [self.nlp(doc.lower()) for doc in iter_docs]
        lemmas = [[word for sent in doc.sentences for word in sent.words] for doc in doc_nlps] # get list of `Words` from `Sentences`

        if filter_postags:
            is_selected_tag = lambda w: w.upos in filter_postags
            lemmas = [list(filter(is_selected_tag,doc)) for doc in lemmas]
        
        lemmas = list(map(lambda s: [w.lemma for w in s], lemmas)) # `Words` to `String`
        
        return lemmas

    def topic_analysis(self, docs_lemmatized, topics_nb=20, passes=50, print_words=0):
        """
        Creates a model topic model using LDA.

        Parameters
        ---------
        docs_lemmatized: List of list of Strings
            List of lemmas representing a document.
            This usually is the result from `lemmatize()` function
        topics_nb: int
            number of topics to distinguish.
            LDA will return a model clustering `topics_nb` topics.
        passes: int
            number of passes to run train the LDA model
        print_words: int
            Will print this amount of words per topic once it is created.
            It will only print if `print_words` is bigger than 0.
        
        Returns
        -------
        LDA trained model and Dictionnary `(model, dict)`
        """
        dictionnary = corpora.Dictionary(docs_lemmatized) # make a dictionnary with all the words
        
        # doc to vector from dict
        doc_term_matrix =[dictionnary.doc2bow(doc) for doc in docs_lemmatized]
        ldamodel = LdaModel(doc_term_matrix, num_topics=topics_nb, id2word=dictionnary, passes=passes)
        
        # Print topics
        if print_words>0:
            for i in ldamodel.print_topics(num_topics=topics_nb, num_words=print_words):
                logging.info(i)
        
        return ldamodel, dictionnary
