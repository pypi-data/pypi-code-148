from __future__ import print_function
import keras
from keras.datasets import cifar100
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from common.metrics_cal import metrics_cal
import numpy as np
import sys
import os


aa = len(sys.argv)
if aa >1:
    lr = float(sys.argv[1])
else:
    lr=0.01

batch_size = 32
num_classes = 100
epochs = 1
data_augmentation = True
num_predictions = 20


# The data, split between train and test sets:
(x_train, y_train), (x_test, y_test) = cifar100.load_data(label_mode='fine')
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# Convert class vectors to binary class matrices.
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

'''
model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

# initiate RMSprop optimizer
#opt = keras.optimizers.RMSprop(learning_rate=0.0001, decay=1e-6)
opt = keras.optimizers.SGD(lr=lr,decay=1e-6,momentum=0.9, nesterov=True)
# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

'''
def save_pr_plot(model_s, title, epochs,save_dir, file_):
    #save_dir = os.path.join(os.getcwd(), 'val')
    #model_name = 'model20epochgamma.h5'
    #weight_name = 'model_weight20epochgamma.h5'
    #model_name = 'model20epochgaussian1.h5'
    #weight_name = 'model_weight[0.05].h5'
    '''
    model_name = '50_keras_cifar10_trained_model.h5'
    weight_name = '20epoch_weight.h5'
    
    model_path = os.path.join(save_dir, model_name)
    weight_path = os.path.join(save_dir, weight_name)
    model_s = load_model(model_path)
    model_s.load_weights(weight_path)
    '''
    x_train_ = x_train.astype('float32')
    x_test_ = x_test.astype('float32')
    x_train_ /= 255
    x_test_ /= 255
    
    predic = model_s.predict(x_test_)
    scala_predic = np.empty(0)
    scala_y_test = np.empty(0)
    for h in range(len(predic)): 
        predic_val = np.argmax(predic[h])
        y_test_val = np.argmax(y_test[h])
        scala_predic = np.hstack([scala_predic,predic_val])
        scala_y_test = np.hstack([scala_y_test,y_test_val])
        
    val = metrics_cal()
    val.metrics_num(scala_y_test, scala_predic,num_classes)
    
    #print('accuracy_arr: ',val.accuracy_arr,'\n confusion_arr: ',val.confusion_arr,'\n precision_arr: ',val.precision_arr,'\n recall_arr: ', val.recall_arr,'\n mcc_arr: ',val.mcc_arr,'\n sensitivity_arr: ',val.sensitivity_arr,'\n specificity_arr: ',val.specificity_arr, file=file_)
    print('accuracy: ',val.accuracy_avg,' confusion: ',val.confusion_avg,' precision: ',val.precision_avg,' recall: ', val.recall_avg,' mcc: ',val.mcc_avg, ' sensitivity: ',val.sensitivity_avg, ' specificity: ',val.specificity_avg, file=file_)  
    #val.metrics_plot(scala_y_test, scala_predic,'Gamma Distn Search epoch',20, save_dir)
    #val.metrics_plot(scala_y_test, scala_predic,'Gaussian Distn Search epoch',1, save_dir)
    val.metrics_plot(scala_y_test, scala_predic, title, epochs, save_dir)
    scores = model_s.evaluate(x_test_, y_test, verbose=1)
    print('Test loss:', scores[0])
    print('Test accuracy:', scores[1])
    print('Test loss:', scores[0], file=file_)
    print('Test accuracy:', scores[1], file=file_)
    return file_
