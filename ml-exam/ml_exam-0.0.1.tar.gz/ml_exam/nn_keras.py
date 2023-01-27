def nn_keras():
    print('''
from keras.datasets import mnist
(train_images,train_labels),(test_images,test_labels) = mnist.load_data()

import pandas as pd
import numpy as np
import cv2 #Computer vision
import matplotlib.pyplot as plt
import os

from sklearn.metrics import accuracy_score

print(train_images.shape)
print(train_labels.shape)
print(test_images.shape)
print(test_labels.shape)

from keras import models
from keras import layers

network = models.Sequential()
network.add(layers.Dense(512,activation='relu',input_shape = (28*28,)))
network.add(layers.Dense(10,activation='softmax'))
network.summary()

#Cost
network.compile(optimizer = 'rmsprop', #Root mean square error 
               loss = 'categorical_crossentropy', #categorical as its multiclass. Sirf 2 classes hote to binary
               metrics = ['accuracy'])

train_images = train_images.reshape((60000,28*28))
train_images = train_images.astype('float32')/255

test_images = test_images.reshape((10000,28*28))
test_images = test_images.astype('float32')/255

from tensorflow.keras.utils import to_categorical
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

print(train_labels.shape)
print(test_labels.shape)

network.fit(train_images,train_labels,epochs = 5, batch_size = 128)


    ''')


nn_keras()
