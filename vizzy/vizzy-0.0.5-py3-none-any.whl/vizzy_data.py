#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from nltk.corpus import stopwords
from nltk.util import ngrams

from sklearn.feature_extraction.text import CountVectorizer
import gensim
from collections import  Counter
import string
from nltk.stem import WordNetLemmatizer,PorterStemmer
from nltk.tokenize import word_tokenize
import pyLDAvis
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
from spacy import displacy
import nltk
from textblob import TextBlob
from textstat import flesch_reading_ease

plt.rcParams.update({'font.size': 18})
plt.rcParams.update({'figure.figsize': [16, 12]})
plt.style.use('seaborn-whitegrid')


# In[ ]:


class vizzy:
    def __init__(self, data, column):
        from nltk.corpus import stopwords
        stopwords = set(stopwords.words('english'))
        data[column] = data[column].apply(lambda x: x.lower())
        data['text_without_stopwords'] = data[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stopwords]))
        self.data = data
        self.column = column
        
        
    def show_char_count(self):
        '''Histogram of the length of your data column in characters'''
        char_plot = self.data[self.column].str.len().hist()
        return char_plot
    
    def show_word_count(self):
        '''Histogram of the length of data column in words'''
        count_plot = self.data[self.column].str.split().map(lambda x: len(x)).hist()
        return count_plot
    
    def show_word_length(self):
        '''Hist of length of words in data column in characters'''
        len_plot = self.data[self.column].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x: np.mean(x)).hist()
        return len_plot
    
    def show_common_stopwords(self):
        '''List of common stopwords in data'''
        stop=set(STOPWORDS)
        corpus=[]
        new= self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]

        from collections import defaultdict
        dic=defaultdict(int)
        for word in corpus:
            if word in STOPWORDS:
                dic[word]+=1
        top=sorted(dic.items(), key=lambda x:x[1],reverse=True)[:10] 
        x,y=zip(*top)
        plot = plt.bar(x,y)
        return plot
    
    def show_common_words(self):
        '''Common words in data'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        counter=Counter(corpus)
        most=counter.most_common()
        x, y=[], []
        for word,count in most[:40]:
            try:
                if (word not in STOPWORDS):
                    x.append(word)
                    y.append(count)
            except:
                x.append(word)
                y.append(count)
        sns.barplot(x=y,y=x)
        
    def show_sentiment(self):
        '''Sentiment in data'''
        text = self.data[self.column]
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        hist = self.data['polarity_score'].hist()
        return hist

    def show_sentiment_cats(self):
        '''Plot data by sentiment (pos, neu, neg)'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        plot = plt.bar(self.data.polarity.value_counts().index, self.data.polarity.value_counts())
        return plot
    
    def show_neg_sentiment(self):
        '''Show negative sentiment'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        results = self.data[self.data['polarity']=='neg'][self.column].head(5)
        return results
    
    def show_pos_sentiment(self):
        '''Show positive sentiment'''
        def polarity(text):
            return TextBlob(text).sentiment.polarity
        self.data['polarity_score']=self.data[self.column].apply(lambda x : polarity(x))
        def sentiment(x):
            if x<0:
                return 'neg'
            elif x==0:
                return 'neu'
            else:
                return 'pos'
        self.data['polarity']=self.data['polarity_score'].map(lambda x: sentiment(x))
        results = self.data[self.data['polarity']=='pos'][self.column].head(5)
        return results
    
    def show_flesch_kincaid(self):
        '''show flesch kincaid score'''
        hist = self.data[self.column].apply(lambda x : flesch_reading_ease(x)).hist()
        return hist
    
    def show_bi_grams(self):
        '''show most common bi-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],2)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        plot = sns.barplot(x=y,y=x)
        return plot
        
    def show_tri_grams(self):
        '''show most common tri-grams'''
        corpus=[]
        new=self.data[self.column].str.split()
        new=new.values.tolist()
        corpus=[word for i in new for word in i]
        def get_top_ngram(corpus, n=None):
            vec = CountVectorizer(ngram_range=(n, n)).fit(corpus)
            bag_of_words = vec.transform(corpus)
            sum_words = bag_of_words.sum(axis=0) 
            words_freq = [(word, sum_words[0, idx]) 
                          for word, idx in vec.vocabulary_.items()]
            words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
            return words_freq[:10]

        top_n_bigrams=get_top_ngram(self.data[self.column],3)[:10]
        x,y=map(list,zip(*top_n_bigrams))
        plot = sns.barplot(x=y,y=x)
        return plot

