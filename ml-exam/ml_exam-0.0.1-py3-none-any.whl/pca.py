def pca():
    print('''
import numpy as np
from sklearn.decomposition import PCA

# define a matrix
A = np.array([[2.5, 2.4], [0.5, 0.7], [2.2, 2.9],[1.9,2.2],[3.1,3],[2.3,2.7],[2,1.6],[1,1.1],[1.5,1.6],[1.1,0.9]])
print(A)

# create the PCA instance
pca = PCA()

# fit on data
pca.fit(A)

# access values and vectors
print(pca.components_.T)

print(pca.explained_variance_)

# transform data
B = pca.transform(A)

print(B)

print(pca.explained_variance_ratio_)

      ''')


pca()
