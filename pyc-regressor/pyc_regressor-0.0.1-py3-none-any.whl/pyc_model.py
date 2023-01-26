import pycaret
import pandas as pd
import numpy as np
from pycaret.regression import *
from pycaret.utils import check_metric

#check the shape of data

class ModelTraining:
    def __init__(self) -> None:
        pass
    def train(data_df,test_df,target_col):
    
        s = setup(data=data_df, target = target_col)
        #compare models
        best_model = compare_models()
        predict_model(best_model)
        save_model(best_model, 'my_model')
        loaded_model = load_model('my_model')

        y_pred = predict_model(best_model,data=test_df)
        r2 = check_metric(test_df[target_col], y_pred.Label, 'R2')
        print(" the R2 score of model is : ", r2)

        return y_pred ,loaded_model

    def loadmodel(path):
        return load_model(path)

    def predict(test_df,best_model):
        y_pred = predict_model(best_model,data=test_df)
        
        return y_pred





