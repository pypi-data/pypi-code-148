import pandas as pd
import pycaret
from pycaret.regression import * 
from pyc.pyc_model import *




class ModelPrediction:
    def __init__(self) -> None:
        pass

    def createmodel(self,model_str):
        my_model = create_model(model_str)
        return my_model

    def tunemodel(self,model_str):
        c_model = self.createmodel(model_str)
        return tune_model(estimator=c_model,n_iter=50)

    def evalmodel(self,model_str):
        c_model = self.createmodel(model_str)
        return evaluate_model(estimator=c_model) 

    def modelprediction(self,test_df):

        y_pred = predict_model(self.loadmodel(),data=test_df)

        

        return y_pred

    def savemodel(my_model):
        save_model(my_model, 'my_model_pipeline')
        with open('pipeline_flow.txt','w') as file:
            file.write(str(my_model))

    def loadmodel():
        return load_model('my_model_pipeline')
        #return load_model('my_model_pipeline')



 





