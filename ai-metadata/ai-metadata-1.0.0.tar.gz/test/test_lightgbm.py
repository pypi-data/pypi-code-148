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
from ai_metadata import MetadataModel, ModelSerialization, MiningFunction

seed = 123456
test_size = 0.33


def test_classification():
    from lightgbm import LGBMClassifier

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    classifier = LGBMClassifier(random_state=seed)
    classifier = classifier.fit(X_train, y_train, eval_set=[(X_test, y_test)])

    model = MetadataModel.wrap(classifier,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'] == [
        {
            "name": "sepal length (cm)",
            "sample": 5.7,
            "type": "float64"
        },
        {
            "name": "sepal width (cm)",
            "sample": 4.4,
            "type": "float64"
        },
        {
            "name": "petal length (cm)",
            "sample": 1.5,
            "type": "float64"
        },
        {
            "name": "petal width (cm)",
            "sample": 0.4,
            "type": "float64"
        }
    ]
    assert model_metadata['targets'] == [
        {
            "name": "target",
            "sample": 0,
            "type": "int64"
        }
    ]

    prediction = model.predict([[x['sample'] for x in model_metadata['inputs']]])
    print(f"prediction: {prediction.tolist()}")
    assert prediction.tolist() == [0]

    proba = model.predict_proba([[x['sample'] for x in model_metadata['inputs']]])
    print(f"proba: {proba.tolist()}")
    assert proba.tolist()
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.JOBLIB
    assert model_metadata['algorithm'] == 'LGBMClassifier'
    assert model.save_model('./lightgbm-cls')


def test_regression():
    from lightgbm import LGBMRegressor

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    regressor = LGBMRegressor(num_leaves=31,
                              learning_rate=0.05,
                              n_estimators=20,
                              random_state=seed)
    regressor.fit(X_train, y_train, eval_set=[(X_test, y_test)], eval_metric='l1', early_stopping_rounds=5)

    model = MetadataModel.wrap(regressor,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print(model.model_metadata(as_json=True, indent=4))
    assert model_metadata['inputs'] == [
        {
            "name": None,
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
            "type": "float64",
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

    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    print(f"prediction: {prediction.tolist()}")
    assert prediction.tolist()
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] == ModelSerialization.JOBLIB
    assert model_metadata['algorithm'] == 'LGBMRegressor'
    assert model.save_model('./lightgbm-reg')


def test_raw_classification():
    import lightgbm as lgb

    X, y = datasets.load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    params = {
        'task': 'train',
        'boosting_type': 'gbdt',
        'objective': 'multiclass',
        'metric': {'multi_logloss'},
        'num_leaves': 63,
        'learning_rate': 0.1,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.9,
        'bagging_freq': 0,
        'verbose': 0,
        'num_class': 3
    }

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    booster = lgb.train(params, lgb_train, valid_sets=lgb_eval)
    model = MetadataModel.wrap(booster,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print("With test data: " + model.model_metadata(as_json=True, indent=4))
    prediction = model.predict([[x['sample'] for x in model_metadata['inputs']]])
    proba = model.predict_proba([[x['sample'] for x in model_metadata['inputs']]])
    print(f"prediction: {prediction.tolist()}")
    print(f"proba: {proba.tolist()}")
    assert prediction.tolist() == [0]
    assert proba.shape == (1, 3)
    assert model_metadata['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata['serialization'] == ModelSerialization.LIGHTGBM
    assert model_metadata['algorithm'] == 'Booster'
    assert model_metadata['metrics'] != {}

    model = MetadataModel.wrap(booster)
    model_metadata_no_test_data = model.model_metadata()

    print("Without test data: " + model.model_metadata(as_json=True, indent=4))
    assert model_metadata_no_test_data['function_name'] == MiningFunction.CLASSIFICATION
    assert model_metadata_no_test_data['serialization'] == ModelSerialization.LIGHTGBM
    assert model_metadata_no_test_data['metrics'] == {}
    assert model.save_model('./lightgbm-raw-cls')


def test_raw_regression():
    import lightgbm as lgb

    X, y = datasets.load_boston(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed)

    params = {
        'boosting_type': 'gbdt',
        'objective': 'regression',
        'metric': {'l2', 'l1'},
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': 0}
    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    booster = lgb.train(params, lgb_train, valid_sets=lgb_eval)
    model = MetadataModel.wrap(booster,
                               x_test=X_test,
                               y_test=y_test)
    model_metadata = model.model_metadata()

    print("With test data: " + model.model_metadata(as_json=True, indent=4))
    prediction = model.predict(model_metadata['inputs'][0]['sample'])
    print(f"prediction: {prediction.tolist()}")
    assert prediction.tolist()
    assert model_metadata['function_name'] == MiningFunction.REGRESSION
    assert model_metadata['serialization'] == ModelSerialization.LIGHTGBM
    assert model_metadata['algorithm'] == 'Booster'
    assert model_metadata['metrics'] != {}

    model = MetadataModel.wrap(booster)
    model_metadata_no_test_data = model.model_metadata()

    print("Without test data: " + model.model_metadata(as_json=True, indent=4))
    assert model_metadata_no_test_data['function_name'] == MiningFunction.REGRESSION
    assert model_metadata_no_test_data['serialization'] == ModelSerialization.LIGHTGBM
    assert model_metadata_no_test_data['metrics'] == {}
    assert model.save_model('./lightgbm-raw-reg')

