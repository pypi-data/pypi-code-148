import pandas as pd
import sklearn
from huble.sklearn.metrics import log_metrics, upload

def evaluate_model(model, test_dataset, target_column, task):
    y_test = test_dataset['target_column']
    X_test = test_dataset.drop(['taregt_column'], axis=1)
    y_pred = model.predict(X_test)
    metrics = log_metrics(y_test, y_pred, task)
    upload(metrics)
    return metrics
