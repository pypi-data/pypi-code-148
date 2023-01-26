import pycaret
import pandas as pd
from pycaret.regression import *
from sklearn.model_selection import mean_squared_error


#check the shape of data

class ModelTraining:
    def __init__(self) -> None:
        pass
    def modeltraining(data_df,target_col):
    
        #s = setup(df, target = 'SalePrice', session_id = 123, log_experiment = True, experiment_name = 'exp1')
        s = setup(data=data_df, target = target_col)
        #compare models
        best_model = compare_models()
        with open ('best_model.txt', 'w') as file:  
            file.write(str(best_model))  

        return compare_models()




#best_model = compare_models()

#print(best_model)

# compare models
#best_model = compare_models()
#with open ('all_models_compare.txt', 'w') as file:  
    #file.write(str(best_model))  

# save model
#save_model(best_model, 'my_first_pipeline')


