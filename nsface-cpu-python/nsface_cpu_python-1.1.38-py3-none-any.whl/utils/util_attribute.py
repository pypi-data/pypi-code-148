import os
import numpy as np   
    
    
def get_pred(sf_gender, sf_age):#,resize):
    age_female = sf_age[:,:101]
    age_male = sf_age[:,101:]

    #p_female = np.reshape(sf_gender[:,0],(resize,1))*age_female
    #p_male = np.reshape(sf_gender[:,1],(resize,1))*age_male

    p_female = sf_gender[:,0][0]*age_female
    p_male = sf_gender[:,1][0]*age_male

    p_age = p_female+p_male

    pred_gender = np.argmax(sf_gender)#,axis=1)
    pred_age = np.argmax(p_age)#,axis=1)


    return pred_gender, pred_age,sf_gender