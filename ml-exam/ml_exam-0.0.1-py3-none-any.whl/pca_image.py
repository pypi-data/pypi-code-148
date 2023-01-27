def pca_image():
    print('''
    import pandas as pd
import matplotlib.pyplot as plt
import os
import cv2 image = "./images"
os.listdir(image)
def load_image(image):
    img = []
    for i in os.listdir(image):
        img1 = cv2.imread(os.path.join(image,i))
        img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img1 = cv2.resize(img1,(256,256))
        img.append(img1)
    return img def get_array(image):
    arrays = np.array(load_image(image))
    arrays = np.reshape(arrays,(arrays.shape[0],arrays.shape[1]*arrays.shape[2]))
    return arrays,arrays.shape[0] x,shape = get_array(image)
x.shape x = x.astype('float32')/255
x from sklearn.decomposition import PCA
pca = PCA()
pca.fit(x)
print(pca.components_.T)
print(pca.explained_variance_)
print(pca.explained_variance_ratio_)
plt.imshow(pca.components_[0].reshape(256,256))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
x1 = pca.transform(x)
y=np.dot(x1,pca.components_)
plt.imshow(y[0].reshape(256,256))
    ''')


pca_image()
