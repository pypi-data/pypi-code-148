#!/usr/bin/env python
# coding: utf-8

# In[1]:


import spacy
import pandas as pd


# In[5]:


class space_wrap:
    def __init__(self, data, column, model):
        self.data = data
        self.column = column
        self.model = model
    
    def create_df(self):
        df = pd.DataFrame(self.data)
        df = pd.DataFrame(df[self.column])
        df[self.column] = df[self.column].astype(str).apply(lambda x: x.lower())
        rows = []
        nlp = spacy.load(self.model)

        # iterate over the rows of the dataframe
        for i, row in df.iterrows():
            doc = nlp(row['text'])
            # iterate over the tokens
            for token in doc:
                # add a new row to the list with the word, the original sentence, the start index, the end index and the entity
                rows.append([token.text, row['text'], token.i, token.i+1, token.ent_type_])

        # create a new dataframe with the desired columns
        df_new = pd.DataFrame(rows, columns=['token', 'text', 'start','end','entity'])
        return df_new




