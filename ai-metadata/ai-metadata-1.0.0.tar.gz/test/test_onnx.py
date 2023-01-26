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

from sklearn import datasets
from sklearn.model_selection import train_test_split
from ai_metadata import MetadataModel, MiningFunction, ModelSerialization


seed = 123456


def test_classification():
    from sklearn.linear_model import LogisticRegression
    import onnxmltools
    from onnxmltools.convert.common.data_types import FloatTensorType

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)

    clf = LogisticRegression(random_state=seed)
    clf.fit(X_train, y_train)

    # use a raw model object
    model = MetadataModel.wrap(clf,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print("Raw model object:" + model.model_metadata(as_json=True, indent=4))
    assert model_metadata['framework'] == 'Scikit-learn'

    initial_types = [('X', FloatTensorType([None, X_test.shape[1]]))]
    onnx_model = onnxmltools.convert_sklearn(clf, initial_types=initial_types)

    model_path = './logreg_iris.onnx'
    with open(model_path, "wb") as f:
        f.write(onnx_model.SerializeToString())

    # use a file path
    model = MetadataModel.wrap(model_path,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print("ONNX model path:" + model.model_metadata(as_json=True, indent=4))
    assert model_metadata['framework'] == 'ONNX'

    # use an onnx.ModelProto object
    model = MetadataModel.wrap(onnx_model,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print("ONNX model object:" + model.model_metadata(as_json=True, indent=4))

    assert model_metadata['inputs'] == [
        {
            "name": "X",
            "type": "tensor(float)",
            "shape": [
                None,
                4
            ],
            "sample": [
                [
                    5.7,
                    4.4,
                    1.5,
                    0.4
                ]
            ]
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": "output_label",
            "type": "tensor(int64)",
            "shape": [
                None
            ]
        },
        {
            "name": "output_probability",
            "type": "seq(map(int64,tensor(float)))",
            "shape": []
        }
    ]

    prediction = model.predict({x['name']: x['sample'] for x in model_metadata['inputs']})
    print(f"prediction={prediction.tolist()}")
    assert prediction.tolist()
    proba = model.predict_proba({x['name']: x['sample'] for x in model_metadata['inputs']})
    print(f"proba={proba}")
    assert proba
    assert model_metadata['metrics']
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.ONNX
    assert model.save_model('./onnx-cls.onnx')


def test_regression():
    from lightgbm import LGBMRegressor
    import onnxmltools
    from onnxmltools.convert.common.data_types import FloatTensorType

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=seed)
    lg = LGBMRegressor(num_leaves=31,
                       learning_rate=0.05,
                       n_estimators=20)
    lg.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l1', early_stopping_rounds=5)

    # use a raw model object
    model = MetadataModel.wrap(lg,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))
    model_metadata['framework'] == 'LightGBM'

    initial_types = [('X', FloatTensorType([None, X_test.shape[1]]))]
    onnx_model = onnxmltools.convert_lightgbm(lg, initial_types=initial_types)

    # use an onnx.ModelProto object
    model = MetadataModel.wrap(onnx_model,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()
    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'] == [
        {
            "name": "X",
            "type": "tensor(float)",
            "shape": [
                None,
                13
            ],
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
            ]
        }
    ]
    assert model_metadata['outputs'] == [
        {
            "name": "variable",
            "type": "tensor(float)",
            "shape": [
                None,
                1
            ]
        }
    ]
    prediction = model.predict({x['name']: x['sample'] for x in model_metadata['inputs']})
    print(f"variable: {prediction.tolist()}")
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] == ModelSerialization.ONNX
    assert model.save_model('./onnx-reg.onnx')


def test_dnn_onnx():
    import numpy as np
    import onnxmltools
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
    onnx_model = onnxmltools.convert_keras(model, model.name)

    # use an onnx.ModelProto object
    model = MetadataModel.wrap(onnx_model,
                               x_test=x_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print("ONNX model: " + model.model_metadata(as_json=True, indent=4))
    prediction = model.predict({x['name']: x['sample'] for x in model_metadata['inputs']})
    print(f"variable: {prediction.tolist()}")
    assert prediction.tolist()
    assert model_metadata['metrics']
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.ONNX
    assert model.save_model('./onnx-dnn.onnx')

