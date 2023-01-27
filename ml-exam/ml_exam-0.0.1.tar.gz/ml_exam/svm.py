def svm():
    print('''
from sklearn.svm import SVC
import numpy as np

X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
y = np.array([1, 1, 2, 2])

svm_one = SVC()

svm_one.fit(X,y)

predict = svm_one.predict(X)

from sklearn.metrics import confusion_matrix

confusion_matrix(y,predict)

import seaborn as sns

sns.heatmap(confusion_matrix(y, predict), annot=True)

svm_one.support_vectors_

    
    ''')


svm()
