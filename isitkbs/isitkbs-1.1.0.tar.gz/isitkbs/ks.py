import pickle
import os
from nltk import everygrams
import matplotlib.pyplot as plt
import pandas as pd
import re
import string

import warnings
warnings.filterwarnings("ignore")

class isitkbs(object):
    
    def __init__(self, model='randomforest'):
        self.model = model
    # Especifica qual modelo deve ser utilizado
    # Por padrão, usa-se o randomForest

    # Função para determinar se uma palavra é keyboardsmashing
    # A entrada deve ser uma palavra
    def wordkbs(self, input_data):
        if not isinstance(input_data, str):
            raise TypeError("input_data must be a string")

        modelpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), f'models/{self.model}.pkl')
        vectpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models/tfid_vectorizer.pkl')

        trained_model = pickle.load(open(modelpath, 'rb'))
        vectorizer = pickle.load(open(vectpath, 'rb'))

        if (len(input_data) <= 2):
            return 0
        
        word = input_data.translate(str.maketrans("", "", string.punctuation))
        word = [word]
        input_ngrams = []

        for i in range(len(word)):
            ngram = map(''.join, list(everygrams(word[i], 2, 4)))
            input_ngrams.extend(ngram)

        predprob = trained_model.predict_proba(
            vectorizer.transform(input_ngrams))[:, 1]

        prob = sum(predprob)/len(input_ngrams)
        if (prob >= 0.5):
            return 1
        else:
            return 0

    # Função para determinar quais são os keyboard smashing em uma frase
    # A entrada deve ser uma string ou uma lista de palavras
    def sentkbs(self, input_data):
        mashs = []

        if type(input_data) != str and type(input_data) != list:
            return mashs

        try:
            words = input_data.split()
        except:
            words = input_data

        res = 0
        for i in range(len(words)):
            if type(words[i]) == str:
                if ' ' in words[i]:
                    mashs_partial = self.sentkbs(words[i])
                    mashs.append(mashs_partial)
                else:
                    res = self.wordkbs(words[i])
            else:
                continue
            if res == 1:
                mashs.append(words[i])

        return mashs

    # Função que mostra a frequência de caracteres em keyboard smashing
    # A entrada deve ser uma string ou uma lista de string
    def freqkbs(self, input_data, graph=0):

        cont_char = {}

        data = self.sentkbs(input_data)
        data = ' '.join(data)

        if (len(data) != 0):
            data = re.sub(r'[^\w\s]', '', data)
            sing_char = set(data)

            for i in sing_char:
                cont_char[i] = data.count(i)

            cont_char = dict(sorted(cont_char.items()))

            try:
                del cont_char[' ']
            except:
                pass

            # Plota gráfico se graph = 1 na chamda da função
            if (graph == 1):
                self.__freqgraph(cont_char)

        return cont_char

    def __freqgraph(self, cont_char):
        # Determina eixo x e eixo y
        x_axis = list(cont_char.keys())
        y_axis = list(cont_char.values())

        # Nomeia os eixos
        plt.xlabel('Caracteres')
        plt.ylabel('Frequência')

        # Plota o gráfico
        plt.bar(x_axis, y_axis)

    def replacekbs(self, input_data, value=None, inplace=False, just_word=False):
        """ 
        Parâmetros:
        dataframe: dataframe pandas do qual os keyboard smashing vão ser substituidos.
        value: string que vai substituir os keyboard smashings, caso seja uma string vazia as linhas que apresentarem kbs serão removidas do dataframe
        inplace: se as substituições serão feitas no próprio dataframe dos parâmetros (True) ou será retornada uma cópia do df (False)
        just_word: se False, a posição toda do dataframe é substituído por value, se True somente o kbs presente na posição é substituido
        Ex: "This isdas test" -> "KBS" (just_word False)
                              -> "This KBS test" (just_word True)
        """
        value = value or "itskbs"

        """ 
        Se o tipo de entrada for um dataframe pandas, a função __dataframe é chamada para fazer o tratamento
        """
        if type(input_data) == pd.DataFrame:

            df = input_data.copy(deep=False) if inplace else input_data.copy()
            return self.__dataframe(df, value, just_word)

        """ 
        Se o tipo de entrada for uma lista ou uma string de palavras, a função __listOrString é chamada
        """
        if (type(input_data) == str or type(input_data) == list):
            return self.__listOrString(input_data, value, just_word)

    def __dataframe(self, df, value, just_word):
        wordskbs = []
        nRow = df.shape[0]
        nCol = df.shape[1]
        mashsIndex = []
        for row in range(nRow):
            for col in range(nCol):
                wordskbs = self.sentkbs(df.iloc[row, col])
                if (len(wordskbs) != 0):
                    if (just_word == False):
                        if(value == 'itskbs'):
                            mashsIndex.append(row)
                        else:
                            df.iloc[row, col] = value
                    else:
                        df.iloc[row, col] = self.replacekbs(
                            df.iloc[row, col], value)
        df.drop(mashsIndex, axis=0, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def __listOrString(self, input_data, value, just_word):
        isList = True
        if (type(input_data) != list):
            isList = False
            input_data = input_data.split()

        wordskbs = self.sentkbs(input_data)
        output_data = []
        for i in input_data:
            if ' ' in i:
                sent = self.__listOrString(i, value, just_word)
                if just_word:
                    output_data.append(sent)
                    continue
                elif sent != i:
                    output_data.append(value)
                    continue
            if (i not in wordskbs):
                output_data.append(i)
            elif (value != 'itskbs'):
                output_data.append(value)

        if (isList == False):
            output_data = ' '.join(output_data)
        return output_data