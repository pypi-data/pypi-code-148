def adaboost():
    return """
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import AdaBoostClassifier
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.ensemble import GradientBoostingClassifier
            from xgboost import XGBClassifier
            from sklearn.metrics import accuracy_score
            from sklearn.model_selection import train_test_split

            data = pd.read_csv('bank_marketing.csv')

            X = data[['age','marital','ever_defaulted','housing_loan','Personal_loan']]
            Y = data[['y']]
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20, 
            random_state = 42)
            test_df = pd.concat ([X_test,y_test],axis =1 )

            abc = AdaBoostClassifier(random_state=0)
            abc_model = abc.fit(X_train, y_train)
            abc_pred = abc_model.predict(X_test)
            accuracy_score(y_test, abc_pred)"""
def xgb():
    return """ 
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import AdaBoostClassifier
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.ensemble import GradientBoostingClassifier
            from xgboost import XGBClassifier
            from sklearn.metrics import accuracy_score
            from sklearn.model_selection import train_test_split

            data = pd.read_csv('bank_marketing.csv')

            X = data[['age','marital','ever_defaulted','housing_loan','Personal_loan']]
            Y = data[['y']]
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20, 
            random_state = 42)
            test_df = pd.concat ([X_test,y_test],axis =1 )

            model = XGBClassifier()
            model.fit(X_train,y_train)
            xgbc_pred = model.predict(X_test)
            accuracy_score(y_test, xgbc_pred)"""

def gradient():
    return """
            import pandas as pd
            
            from sklearn.model_selection import train_test_split
            
            from sklearn.ensemble import AdaBoostClassifier
            
            from sklearn.ensemble import RandomForestClassifier
            
            from sklearn.ensemble import GradientBoostingClassifier
            
            from xgboost import XGBClassifier
            
            from sklearn.metrics import accuracy_score
            
            from sklearn.model_selection import train_test_split


            
            data = pd.read_csv('bank_marketing.csv')


            
            X = data[['age','marital','ever_defaulted','housing_loan','Personal_loan']]
            
            Y = data[['y']]
            
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20, 
            
            random_state = 42)
            
            test_df = pd.concat ([X_test,y_test],axis =1 )
            
            gbcl = GradientBoostingClassifier(random_state = 42)
            
            gbcl.fit(X_train, y_train)
            
            gbcl_pred = gbcl.predict(X_test)
            
            accuracy_score(y_test, gbcl_pred) """

def randomforest():
    return """
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import AdaBoostClassifier
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.ensemble import GradientBoostingClassifier
            from xgboost import XGBClassifier
            from sklearn.metrics import accuracy_score
            from sklearn.model_selection import train_test_split

            data = pd.read_csv('bank_marketing.csv')

            X = data[['age','marital','ever_defaulted','housing_loan','Personal_loan']]
            Y = data[['y']]
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20, 
            random_state = 42)
            test_df = pd.concat ([X_test,y_test],axis =1 )

            clf = RandomForestClassifier(random_state = 42) 
            clf.fit(X_train, y_train)
            rf_pred = clf.predict(X_test)
            accuracy_score(y_test, rf_pred)""" 

def A_ens():
     return """
            import pandas as pd
            from sklearn.preprocessing import LabelEncoder
            le = LabelEncoder()
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
            from sklearn.model_selection import train_test_split
            from sklearn.ensemble import AdaBoostClassifier
            from sklearn.metrics import accuracy_score
            from sklearn.ensemble import GradientBoostingClassifier
            from sklearn.ensemble import RandomForestClassifier

            !pip install tensorflow

            data = pd.read_csv('loanapproval.csv')
            data.head()

            # Checking for Missing values
            data.isnull().sum()
            # convert string variable to One Hot Encoding
            dummyfied_data = data.apply(le.fit_transform)
            dummyfied_data.head()

            # Scalling the numeric column
            col_to_scale =['age']
            dummyfied_data[col_to_scale] = scaler.fit_transform(dummyfied_data[col_to_scale])
            dummyfied_data.head()
            X = dummyfied_data.drop('Loan_approved',axis = 1)
            Y = dummyfied_data[['Loan_approved']]


            ## ADABOOST
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20,
            random_state = 42)
            test_df = pd.concat ([X_test,y_test],axis =1 )
            # Adaboost classifier
            abc = AdaBoostClassifier(random_state=0)
            abc_model = abc.fit(X_train, y_train)
            abc_pred = abc_model.predict(X_test)
            test_df['abc_pred'] = abc_pred
            score = accuracy_score(y_test, abc_pred)
            X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size = 0.20,
            random_state = 42)
            test_df = pd.concat ([X_test,y_test],axis =1 )
            # Adaboost classifier
            abc = AdaBoostClassifier(random_state=0)
            abc_model = abc.fit(X_train, y_train)
            abc_pred = abc_model.predict(X_test)
            test_df['abc_pred'] = abc_pred
            score = accuracy_score(y_test, abc_pred)


            ##RANDOM FOREST
            # creating a RF classifier, training a random Forest model
            clf = RandomForestClassifier(random_state = 42)
            clf.fit(X_train, y_train)
            # Predicting on Test data and checking the accuracy. This can be extended to
            rf_pred = clf.predict(X_test)
            test_df['rf_pred'] = rf_pred
            score = accuracy_score(y_test, rf_pred)
            score 

            ##GBM
            # creating gbc
            gbc = GradientBoostingClassifier(random_state = 42)
            gbc.fit(X_train, y_train)
            # Predicting on Test data and checking the accuracy. This can be extended to
            # train data as well
            gbc_pred = gbc.predict(X_test)
            test_df['gbcl_pred'] = gbc_pred
            score = accuracy_score(y_test, gbc_pred)
            score 

            #!pip install xgboost

            ##XGB
            from xgboost import XGBClassifier
            xgb = XGBClassifier()
            xgb.fit(X_train, y_train)
            y_pred = xgb.predict(X_test)
            test_df['xgb_pred']=y_pred
            score=accuracy_score(y_test,y_pred)
            score

            #ANN
            import tensorflow as tf
            from tensorflow import keras
            from keras.layers import Dense
            from keras.optimizers import Adam
            model = keras.Sequential()
            model.add(Dense(10,input_shape=(5,), activation='relu'))
            model.add(Dense(1,activation='sigmoid'))
            history = model.compile(optimizer="Adam", loss='binary_crossentropy' , metrics=['accuracy'])
            model.fit(X_train,y_train,epochs=10)
            import numpy as np
            y_pred = model.predict(X_test)
            y_pred = np.where(y_pred>0.5,1,0)
            test_df['ann_pred']=y_pred
            score=accuracy_score(y_test,y_pred)
            score

            ##ENSEMBLING
            # Ensemble the ensembles
            column_names = ['abc_pred', 'rf_pred', 'gbcl_pred','xgb_pred','ann_pred']
            test_df['sum'] = test_df[column_names].sum(axis=1)
            test_df['ensembeled_pred'] = [1 if x > 3 else 0 for x in test_df['sum'] ]
            score = accuracy_score(y_test, test_df['ensembeled_pred'])
            score

            ##IF SIR ASKS TO DO THE SAME FOR TRAIN
            new_df = pd.DataFrame()

            new_df['abc']=abc_model.predict(X_train)
            accuracy_score(y_train,abc_model.predict(X_train))

            new_df['rf']=clf.predict(X_train)
            accuracy_score(y_train,clf.predict(X_train))

            new_df['gbc']=gbc.predict(X_train)
            accuracy_score(y_train,gbc.predict(X_train))

            new_df['xgb']=xgb.predict(X_train)
            accuracy_score(y_train,xgb.predict(X_train))

            y_pred=model.predict(X_train)
            y_pred = np.where(y_pred>0.5,1,0)
            new_df['ann']=y_pred
            score=accuracy_score(y_train,y_pred)
            accuracy_score(y_train,y_pred)

            column_names = ['abc', 'rf', 'gbc','xgb','ann']
            new_df['sum'] = new_df[column_names].sum(axis=1)
            new_df['ensembeled_pred'] = [1 if x >= 3 else 0 for x in new_df['sum'] ]
            score = accuracy_score(y_train, new_df['ensembeled_pred'])
            score

            new_df.to_excel('./Train.xlsx', encoding='utf-8')
            new_df

            score = accuracy_score(y_train, new_df['ensembeled_pred'])
            score"""


     