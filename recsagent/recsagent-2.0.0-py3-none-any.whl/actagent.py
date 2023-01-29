#!/usr/bin/env python3
import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm
from helperagent import Helper
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import multiprocessing

# More ML Models
import xgboost as xgb
import xgboost
import sklearn
import statsmodels
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier
import shap as shap

###################################################################################################
# Activity agent ##################################################################################
###################################################################################################  

class Activity_Agent:
    def __init__(self, activity_input_df):
        self.input = activity_input_df

    # train test split
        # -------------------------------------------------------------------------------------------
    def get_Xtest(self, df, date, time_delta='all', target='activity'):
        import pandas as pd
        from helper_functions import Helper

        helper = Helper()

        tomorrow = (pd.to_datetime(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        if time_delta == 'all':
            output = df.loc[pd.to_datetime(tomorrow):, df.columns != target]
        else:
            df = helper.get_timespan(df, tomorrow, time_delta)
            output = df.loc[:, df.columns != target]
        return output

    def get_ytest(self, df, date, time_delta='all', target='activity'):
        import pandas as pd
        from helper_functions import Helper

        helper = Helper()

        tomorrow = (pd.to_datetime(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        if time_delta == 'all':
            output = df.loc[pd.to_datetime(tomorrow):, target]
        else:
            output = helper.get_timespan(df, tomorrow, time_delta)[target]
        return output

    def get_Xtrain(self, df, date, start=-30, target='activity'):
        import pandas as pd

        if type(start) == int:
            start = pd.to_datetime(date) + pd.Timedelta(days= start)
            start = pd.to_datetime('2022-12-31') if start < pd.to_datetime('2022-12-31') else start
        else:
            start = pd.to_datetime(start)

        return df.loc[start:date, df.columns != target]


    def get_ytrain(self, df, date, start=-30, target='activity'):
        import pandas as pd

        if type(start) == int:
            start = pd.to_datetime(date) + pd.Timedelta(days= start)
            start = pd.to_datetime('2022-12-31') if start < pd.to_datetime('2022-12-31') else start
        else:
            start = pd.to_datetime(start)
        return df.loc[start:date, target]
    
    #train start: the day from which training starts
    def get_train_start(self, df):
        import datetime
        end_date = min(df.index) + datetime.timedelta(days=3)
        # determine train_start date 
        return str(end_date)[:10]

    def train_test_split(self, df, date, train_start=-30, test_delta='all', target='activity'):
        if train_start == '':
            train_start = self.get_train_start(df)
        X_train = self.get_Xtrain(df, date, start=train_start, target=target)
        y_train = self.get_ytrain(df, date, start=train_start, target=target)
        X_test = self.get_Xtest(df, date, time_delta=test_delta, target=target)
        y_test = self.get_ytest(df, date, time_delta=test_delta, target=target)
        X_test = X_test.fillna(0)
        X_train = X_train.fillna(0)
        y_test = y_test.fillna(0)
        y_train = y_train.fillna(0)
        return X_train, y_train, X_test, y_test

    # model training and evaluation
    # -------------------------------------------------------------------------------------------
    def fit_Logit(self, X, y, max_iter=100):
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression(random_state=0, max_iter=max_iter).fit(X, y)

    def fit_knn(self, X, y, n_neighbors=10, leaf_size=30):
        from sklearn.neighbors import KNeighborsClassifier
        return KNeighborsClassifier(n_neighbors=n_neighbors, leaf_size=leaf_size, algorithm="auto", n_jobs=-1).fit(X, y)

    def fit_random_forest(self, X, y, max_depth=10, n_estimators=500, max_features="sqrt"):
        from sklearn.ensemble import RandomForestClassifier
        return RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, max_features=max_features, n_jobs=-1).fit(X, y)

    def fit_ADA(self, X, y, learning_rate=0.1, n_estimators=100):
        from sklearn.ensemble import AdaBoostClassifier
        return AdaBoostClassifier(learning_rate=learning_rate, n_estimators=n_estimators).fit(X, y)

    def fit_XGB(self, X, y, learning_rate=0.1, max_depth=6, reg_lambda=1, reg_alpha=0):
        import xgboost
        return xgboost.XGBClassifier(verbosity=0, use_label_encoder=False, learning_rate=learning_rate, max_depth=max_depth, reg_lambda=reg_lambda, reg_alpha=reg_alpha).fit(X, y)

    def fit_EBM(self, X, y): 
        from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier  
        return ExplainableBoostingClassifier().fit(X,y)

    def fit_smLogit(self, X, y):
        import statsmodels
        return statsmodels.api.Logit(y, X).fit(disp=False)
    
    def fit(self, X, y, model_type, **args):
        model = None
        if model_type == "logit":
            model = self.fit_Logit(X, y, **args)
        elif model_type == "ada":
            model = self.fit_ADA(X, y, **args)
        elif model_type == "knn":
            model = self.fit_knn(X, y, **args)
        elif model_type == "random forest":
            model = self.fit_random_forest(X, y, **args)
        elif model_type == "xgboost":
            model = self.fit_XGB(X, y, **args)
        elif model_type == "ebm":
            model = self.fit_EBM(X,y, **args)
        elif model_type == "logit_sm":
            model = self.fit_smLogit(X, y)
        else:
            raise InputError("Unknown model type.")
        return model
    
    def predict(self, model, X):
        import sklearn
        import statsmodels
        from interpret.glassbox.ebm.ebm import ExplainableBoostingClassifier     
        from sklearn.linear_model import LogisticRegression
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.ensemble import AdaBoostClassifier
        import xgboost
        if type(model) == sklearn.linear_model.LogisticRegression:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) == sklearn.neighbors._classification.KNeighborsClassifier:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) == sklearn.ensemble._forest.RandomForestClassifier:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) ==  sklearn.ensemble._weight_boosting.AdaBoostClassifier:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) == xgboost.sklearn.XGBClassifier:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) == ExplainableBoostingClassifier:
            y_hat = model.predict_proba(X)[:,1]

        elif type(model) == statsmodels.discrete.discrete_model.BinaryResultsWrapper:
            y_hat = model.predict(X)

        else:
            raise InputError("Unknown model type.")

        y_hat = pd.Series(y_hat, index=X.index)

        return y_hat

    def auc(self, y_true, y_hat):
        import sklearn.metrics
        try:
            return sklearn.metrics.roc_auc_score(y_true, y_hat)
        except ValueError:
            pass
    
    def plot_model_performance(self, auc_train, auc_test, ylim="default"):
        import matplotlib.pyplot as plt

        plt.plot(list(auc_train.keys()), list(auc_train.values()))
        plt.plot(list(auc_train.keys()), list(auc_test.values()))
        plt.xticks(list(auc_train.keys()), " ")
        plt.ylim(ylim) if ylim != "default" else None

    def evaluate(
            self, df, split_params, model_type, 
        predict_start='2013-11-30', 
        predict_end=-1, return_errors=False,
            xai=False, weather_sel=False, **args
        ):
        import pandas as pd
        import numpy as np
        from tqdm import tqdm

        dates = (
            pd.DataFrame(df.index)
            .set_index(df.index)["last_updated"]
            .apply(lambda date: str(date)[:10])
            .drop_duplicates()
        )
        predict_start = pd.to_datetime(predict_start)
        predict_end = (
            pd.to_datetime(dates.iloc[predict_end])
            if type(predict_end) == int
            else pd.to_datetime(predict_end)
         )
        dates = dates.loc[predict_start:predict_end]
        y_true = []
        y_hat_train = {}
        y_hat_test = []
        y_hat_lime = []
        y_hat_shap = []
        auc_train_dict = {}
        auc_test = []
        xai_time_lime = []
        xai_time_shap = []

        predictions_list = []

        if weather_sel:
            print("Crawl weather data....")
            # Add Weather
            ################################
            from meteostat import Point, Hourly
            from datetime import datetime
            
            #### need to be coded differently!!####################################
            lough = Point(52.766593, -1.223511)
            
            time = df.index.to_series(name="time").tolist()
            weather = Hourly(lough, time[0], time[len(df) - 1])
            weather = weather.fetch()

            from sklearn.impute import KNNImputer
            import numpy as np

            headers = weather.columns.values

            empty_train_columns = []
            for col in weather.columns.values:
                if sum(weather[col].isnull()) == weather.shape[0]:
                    empty_train_columns.append(col)
            headers = np.setdiff1d(headers, empty_train_columns)

            imputer = KNNImputer(missing_values=np.nan, n_neighbors=7, weights="distance")
            weather = imputer.fit_transform(weather)
            scaler = MinMaxScaler()
            weather = scaler.fit_transform(weather)
            weather = pd.DataFrame(weather)
            weather["time"] = time[0:len(weather)]
            df["time"] = time

            weather.columns = np.append(headers, "time")

            df = pd.merge(df, weather, how="right", on="time")
            df = df.set_index("time")
            ################################
        if not xai:
            for date in tqdm(dates):
                errors = {}
                try:
                    X_train, y_train, X_test, y_test = self.train_test_split(
                        df, date, **split_params
                    )

                    # fit model
                    model = self.fit(X_train, y_train, model_type, **args)

                    y_hat_train.update({date: self.predict(model, X_train)})
                    y_hat_test += list(self.predict(model, X_test))

                    # evaluate train data
                    auc_train_dict.update(
                        {date: self.auc(y_train, list(y_hat_train.values())[-1])}
                    )
                    y_true += list(y_test)

                except Exception as e:
                    errors[date] = e
        else:
            print('The explainability approaches in the Activity Agent are being evaluated for model: ' + str(model_type))
            print('Start evaluation with LIME and SHAP')
            import time
            import lime
            from lime import lime_tabular
            import shap as shap

            for date in tqdm(dates):
                errors = {}
                try:
                    X_train, y_train, X_test, y_test = self.train_test_split(
                        df, date, **split_params
                    )

                    # fit model
                    model = self.fit(X_train, y_train, model_type)

                    # self.predict uses predict_proba i.e. we get probability estimates and not classes
                    y_hat_train.update({date: self.predict(model, X_train)})
                    y_hat_test += list(self.predict(model, X_test))

                    # evaluate train data
                    auc_train_dict.update(
                        {date: self.auc(y_train, list(y_hat_train.values())[-1])}
                    )
                    y_true += list(y_test)

                    start_time = time.time()

                    if model_type == "xgboost":
                        booster = model.get_booster()

                        explainer = lime.lime_tabular.LimeTabularExplainer(X_train.values,
                                                                            feature_names=X_train.columns,
                                                                            kernel_width=3, verbose=False)
                    else:
                        explainer = lime_tabular.LimeTabularExplainer(training_data=np.array(X_train),
                                                                        mode="classification",
                                                                        feature_names=X_train.columns,
                                                                        categorical_features=[0])

                    for local in range(len(X_test)):

                        if model_type == "xgboost":
                            exp = explainer.explain_instance(X_test.iloc[local, :].values, model.predict_proba)
                        else:
                            exp = explainer.explain_instance(data_row=X_test.iloc[local], predict_fn=model.predict_proba)

                        y_hat_lime += list(exp.local_pred)


                    # take time for each day:
                    end_time = time.time()
                    difference_time = end_time - start_time

                    xai_time_lime.append(difference_time)
                    # SHAP
                    # ==============================================================================
                    start_time = time.time()

                    if model_type == "logit":
                        X_train_summary = shap.sample(X_train, 100)
                        explainer = shap.KernelExplainer(model.predict_proba, X_train_summary)

                    elif model_type == "ada":
                        X_train_summary = shap.sample(X_train, 100)
                        explainer = shap.KernelExplainer(model.predict_proba, X_train_summary)

                    elif model_type == "knn":
                        X_train_summary = shap.sample(X_train, 100)
                        explainer = shap.KernelExplainer(model.predict_proba, X_train_summary)

                    elif model_type == "random forest":
                        X_train_summary = shap.sample(X_train, 100)
                        explainer = shap.KernelExplainer(model.predict_proba, X_train_summary)

                    elif model_type == "xgboost":
                        explainer = shap.TreeExplainer(model, X_train, model_output='predict_proba')

                    elif model_type == "logit_sm":
                        explainer = shap.TreeExplainer(model.predict, X_train_summary)

                    else:
                        raise InputError("Unknown model type.")

                    base_value = explainer.expected_value[1]  # the mean prediction

                    for local in range(len(X_test)):

                        shap_values = explainer.shap_values(
                            X_test.iloc[local, :])

                        contribution_to_class_1 = np.array(shap_values).sum(axis=1)[1]
                        shap_prediction = base_value + contribution_to_class_1

                        # Prediction from XAI:
                        y_hat_shap += list([shap_prediction])


                    # take time for each day:
                    end_time = time.time()
                    difference_time = end_time - start_time
                    xai_time_shap.append(difference_time)

                except Exception as e:
                    errors[date] = e

        auc_test = self.auc(y_true, y_hat_test)
        auc_train = np.mean(list(auc_train_dict.values()))
        predictions_list.append(y_true)
        predictions_list.append(y_hat_test)
        predictions_list.append(y_hat_lime)
        predictions_list.append(y_hat_shap)

        # Efficiency
        time_mean_lime = np.mean(xai_time_lime)
        time_mean_shap = np.mean(xai_time_shap)
        print('Mean time nedded by appraoches: ' + str(time_mean_lime) + ' ' + str(time_mean_shap))

        if return_errors:
            return auc_train, auc_test, auc_train_dict, time_mean_lime, time_mean_shap, predictions_list, errors
        else:
            return auc_train, auc_test, auc_train_dict, time_mean_lime, time_mean_shap, predictions_list
    
    
    # pipeline function: predicting user activity
    # -------------------------------------------------------------------------------------------
    def pipeline(self, df, date, model_type, split_params, weather_sel=False):

        if weather_sel:

            # Add Weather
            ################################
            from meteostat import Point, Hourly
            from datetime import datetime

            lough = Point(52.766593, -1.223511)
            time = df.index.to_series(name="time").tolist()
            weather = Hourly(lough, time[0], time[len(df) - 1])
            weather = weather.fetch()

            from sklearn.impute import KNNImputer
            import numpy as np

            headers = weather.columns.values

            empty_train_columns = []
            for col in weather.columns.values:
                if sum(weather[col].isnull()) == weather.shape[0]:
                    empty_train_columns.append(col)
            headers = np.setdiff1d(headers, empty_train_columns)

            imputer = KNNImputer(missing_values=np.nan, n_neighbors=7, weights="distance")
            weather = imputer.fit_transform(weather)
            scaler = MinMaxScaler()
            weather = scaler.fit_transform(weather)
            weather = pd.DataFrame(weather)
            weather["time"] = time[0:len(weather)]
            df["time"] = time

            weather.columns = np.append(headers, "time")

            df = pd.merge(df, weather, how="right", on="time")
            df = df.set_index("time")
            ################################

        # train test split
        X_train, y_train, X_test, y_test = self.train_test_split(
            df, date, **split_params
        )

        # fit model
        model = self.fit(X_train, y_train, model_type)

        # predict
        return self.predict(model, X_test)

    # pipeline function: predicting user activity with xai
        # -------------------------------------------------------------------------------------------
    def pipeline_xai(self, df, date, model_type, split_params, weather_sel=False):

        if weather_sel:

            # Add Weather
            ################################
            from meteostat import Point, Hourly
            from datetime import datetime

            lough = Point(52.766593, -1.223511)
            time = df.index.to_series(name="time").tolist()
            weather = Hourly(lough, time[0], time[len(df) - 1])
            weather = weather.fetch()

            from sklearn.impute import KNNImputer
            import numpy as np

            headers = weather.columns.values

            empty_train_columns = []
            for col in weather.columns.values:
                if sum(weather[col].isnull()) == weather.shape[0]:
                    empty_train_columns.append(col)
            headers = np.setdiff1d(headers, empty_train_columns)

            imputer = KNNImputer(missing_values=np.nan, n_neighbors=7, weights="distance")
            weather = imputer.fit_transform(weather)
            scaler = MinMaxScaler()
            weather = scaler.fit_transform(weather)
            weather = pd.DataFrame(weather)
            weather["time"] = time[0:len(weather)]
            df["time"] = time

            weather.columns = np.append(headers, "time")

            df = pd.merge(df, weather, how="right", on="time")
            df = df.set_index("time")

            ################################

        # train test split
        X_train, y_train, X_test, y_test = self.train_test_split(
            df, date, **split_params
        )

        # fit model
        model = self.fit(X_train, y_train, model_type)

        # predict
        return self.predict(model, X_test), X_train, X_test, model