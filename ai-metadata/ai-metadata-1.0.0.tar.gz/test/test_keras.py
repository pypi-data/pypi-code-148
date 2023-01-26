#
# Copyright (c) 2023 AutoDeployAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from sklearn.model_selection import train_test_split
from sklearn import datasets
import numpy as np
import pandas as pd
from ai_metadata import ModelSerialization, MiningFunction, MetadataModel


seed = 123456
test_size = 0.33


def test_classification():
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.optimizers import adam_v2

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    Y = pd.get_dummies(y)
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

    sequential = Sequential()
    sequential.add(Dense(10, input_shape=(4,), activation='relu'))
    sequential.add(Dense(8, activation='relu'))
    sequential.add(Dense(6, activation='relu'))
    sequential.add(Dense(3, activation='softmax'))
    sequential.compile(adam_v2.Adam(lr=0.04), 'categorical_crossentropy', ['accuracy'])
    sequential.fit(X_train, y_train, epochs=10)

    model = MetadataModel.wrap(sequential,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    model_metadata['inputs'][0].pop('name')  # name could vary
    assert model_metadata['inputs'] == [
        {
            "sample": [
                [
                    5.7,
                    4.4,
                    1.5,
                    0.4
                ]
            ],
            "type": "float32",
            "shape": [
                None,
                4
            ],
            "columns": [
                "sepal length (cm)",
                "sepal width (cm)",
                "petal length (cm)",
                "petal width (cm)"
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": 0,
            "sample": 1,
            "type": "uint8"
        },
        {
            "name": 1,
            "sample": 0,
            "type": "uint8"
        },
        {
            "name": 2,
            "sample": 0,
            "type": "uint8"
        }
    ]
    model_metadata['outputs'][0].pop('name')  # name could vary
    assert model_metadata['outputs'] == [
        {
            "type": "float32",
            "shape": [
                None,
                3
            ]
        }
    ]
    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['serialization'] == ModelSerialization.HDF5
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./keras-cls')


def test_classification_tf():
    import tensorflow as tf

    X, y = datasets.load_iris(return_X_y=True)
    Y = pd.get_dummies(y).values
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)

    sequential = tf.keras.Sequential()
    sequential.add(tf.keras.layers.Dense(10, input_shape=(4,), activation='relu'))
    sequential.add(tf.keras.layers.Dense(8, activation='relu'))
    sequential.add(tf.keras.layers.Dense(6, activation='relu'))
    sequential.add(tf.keras.layers.Dense(3, activation='softmax'))
    sequential.compile(tf.keras.optimizers.Adam(lr=0.04), 'categorical_crossentropy', ['accuracy'])
    sequential.fit(X_train, y_train, epochs=10)

    model = MetadataModel.wrap(sequential,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    model_metadata['inputs'][0].pop('name')  # name could vary
    assert model_metadata['inputs'] == [
        {
            "sample": [
                [
                    5.7,
                    4.4,
                    1.5,
                    0.4
                ]
            ],
            "type": "float32",
            "shape": [
                None,
                4
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": [
                1,
                0,
                0
            ],
            "type": "uint8",
            "shape": [
                None,
                3
            ]
        }
    ]
    model_metadata['outputs'][0].pop('name')  # name could vary
    assert model_metadata['outputs'] == [
        {
            "type": "float32",
            "shape": [
                None,
                3
            ]
        }
    ]
    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['serialization'] == ModelSerialization.HDF5
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./tf-keras-cls')


def test_regression():
    from keras.models import Sequential
    from keras.layers import Dense

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    sequential = Sequential()
    sequential.add(Dense(20, input_dim=13, activation='relu'))
    sequential.add(Dense(1))
    sequential.compile(loss='mean_squared_error', optimizer='adam')
    sequential.fit(X_train, y_train, epochs=10)

    model = MetadataModel.wrap(sequential,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    model_metadata['inputs'][0].pop('name')  # name could vary
    assert model_metadata['inputs'] == [
        {
            "sample": [
                [
                    22.5971,
                    0.0,
                    18.1,
                    0.0,
                    0.7,
                    5.0,
                    89.5,
                    1.5184,
                    24.0,
                    666.0,
                    20.2,
                    396.9,
                    31.99
                ]
            ],
            "type": "float32",
            "shape": [
                None,
                13
            ]
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": 7.4,
            "type": "float64"
        }
    ]
    model_metadata['outputs'][0].pop('name')  # name could vary
    assert model_metadata['outputs'] == [
        {
            "type": "float32",
            "shape": [
                None,
                1
            ]
        }
    ]

    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['serialization'] == ModelSerialization.HDF5
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model.save_model('./keras-reg')


def test_dnn():
    from keras.layers import Dense, Dropout, Input
    from keras.layers import Conv2D, MaxPooling2D, Flatten
    from keras.models import Model
    from keras.datasets import mnist
    try:
        from keras.utils import to_categorical
    except ImportError:
        from keras.utils.all_utils import to_categorical

    # load MNIST dataset
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # from sparse label to categorical
    num_labels = len(np.unique(y_train))
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    # reshape and normalize input images
    image_size = x_train.shape[1]
    x_train = np.reshape(x_train, [-1, image_size, image_size, 1])
    x_test = np.reshape(x_test, [-1, image_size, image_size, 1])
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    # network parameters
    input_shape = (image_size, image_size, 1)
    batch_size = 128
    kernel_size = 3
    filters = 64
    dropout = 0.3

    # use functional API to build cnn layers
    inputs = Input(shape=input_shape)
    y = Conv2D(filters=filters,
               kernel_size=kernel_size,
               activation='relu')(inputs)
    y = MaxPooling2D()(y)
    y = Conv2D(filters=filters,
               kernel_size=kernel_size,
               activation='relu')(y)
    y = MaxPooling2D()(y)
    y = Conv2D(filters=filters,
               kernel_size=kernel_size,
               activation='relu')(y)
    # image to vector before connecting to dense layer
    y = Flatten()(y)
    # dropout regularization
    y = Dropout(dropout)(y)
    outputs = Dense(num_labels, activation='softmax')(y)

    # build the model by supplying inputs/outputs
    model = Model(inputs=inputs, outputs=outputs)
    # network model in text
    model.summary()

    # classifier loss, Adam optimizer, classifier accuracy
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # train the model with input images and labels
    model.fit(x_train,
              y_train,
              validation_data=(x_test, y_test),
              epochs=1,
              batch_size=batch_size)

    model = MetadataModel.wrap(model,
                               x_test=x_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'][0]['shape'] == [None, 28, 28, 1]
    assert model_metadata['targets'] == [
        {
            "name": None,
            "sample": [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                1.0,
                0.0,
                0.0
            ],
            "type": "float32",
            "shape": [
                None,
                10
            ]
        }
    ]
    model_metadata['outputs'][0].pop('name')  # name could vary
    assert model_metadata['outputs'] == [
        {
            "type": "float32",
            "shape": [
                None,
                10
            ]
        }
    ]

    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['serialization'] == ModelSerialization.HDF5
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model.save_model('./keras-dnn')

