def lda():
    print('''
import numpy as np
import pandas as pd

df = pd.read_csv("Add path")

df.head()

import sklearn

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda

x = df.iloc[:,0:2]
y = df.iloc[:,2:3]

x

y.shape

LDA = lda(n_components = 1) #Gives us it all on 1 projected line

LDA.fit(x,y)

zscore = LDA.transform(x) 

zscore

y_pred  = LDA.predict(x)
y_pred

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

cm = confusion_matrix(y,y_pred)
print(cm)

accuracy_score(y,y_pred)

''')


lda()
