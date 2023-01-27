def lda_keras():
    print('''
    
import numpy as np 
import matplotlib.pyplot as plt
import os
import cv2
from google.colab import drive


drive.mount('/content/drive')


image=('/content/drive/MyDrive/cat and dog')


os.listdir(image)

def load_img(image):
  img=[]
  for i in os.listdir(image):
    img1=cv2.imread(os.path.join(image,i))
    img1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    img1=cv2.resize(img1,(256,256))
    img.append(img1)
  return img


img2=load_img(image)


len(img2)


img2[4].shape

plt.imshow(img2[4])


def get_arrays(image):
  arrays=np.array(load_img(image))
  arrays=np.reshape(arrays,(arrays.shape[0],arrays.shape[1]*arrays.shape[2]))
  return arrays,arrays.shape[0]


X,shape=get_arrays(image)
X.shape


X=X.astype('float32')/255
X

from keras import layers
from keras import models


network=models.Sequential()
network.add(layers.Dense(512,activation='relu',input_shape=(256*256,)))
network.add(layers.Dense(128,activation='relu',input_shape=(256*256,)))
network.add(layers.Dense(2,activation='softmax'))

network.summary()

network.compile(optimizer='rmsprop',loss='categorical_crossentropy',metrics=['accuracy'])

from tensorflow.keras.utils import to_categorical 

Y=np.array([False,True,False,False,True,True,True]).reshape(-1,1)
Y

Y.shape

Y=to_categorical(Y)

Y.shape

network.fit(X,Y,epochs=5,batch_size=512)



''')


lda_keras()
