
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
# Explainability agent ############################################################################
###################################################################################################    
class Explainability_Agent:
    def __init__(self, model_activity, X_train_activity, X_test_activity, best_hour, model_usage,
               X_train_usage, X_test_usage, model_type):
        self.model_activity = model_activity
        self.model_type = model_type
        self.X_train_activity = X_train_activity
        self.X_test_activity = X_test_activity
        self.best_hour = best_hour
        self.model_usage = model_usage
        self.X_train_usage = X_train_usage
        self.X_test_usage = X_test_usage

    def feature_importance(self):
        if self.model_type == "logit":
            X_train_summary = shap.sample(self.X_train_activity, 100)
            self.explainer_activity = shap.KernelExplainer(self.model_activity.predict_proba, X_train_summary)

        elif self.model_type == "ada":
            X_train_summary = shap.sample(self.X_train_activity, 100)
            self.explainer_activity = shap.KernelExplainer(self.model_activity.predict_proba, X_train_summary)

        elif self.model_type == "knn":
            X_train_summary = shap.sample(self.X_train_activity, 100)
            self.explainer_activity = shap.KernelExplainer(self.model_activity.predict_proba, X_train_summary)

        elif self.model_type == "random forest":

            self.explainer_activity = shap.TreeExplainer(self.model_activity, self.X_train_activity)

        elif self.model_type == "xgboost":
            self.explainer_activity = shap.TreeExplainer(self.model_activity, self.X_train_activity, model_output='predict_proba')
        else:
            raise InputError("Unknown model type.")


        self.shap_values = self.explainer_activity.shap_values(
            self.X_test_activity.iloc[self.best_hour, :])

        feature_names_activity = list(self.X_train_activity.columns.values)

        vals_activity = self.shap_values[1]

        feature_importance_activity = pd.DataFrame(list(zip(feature_names_activity, vals_activity)),
                                                   columns=['col_name', 'feature_importance_vals'])
        feature_importance_activity.sort_values(by=['feature_importance_vals'], ascending=False, inplace=True)

        # usage
        if self.model_type == "logit":
            X_train_summary = shap.sample(self.X_train_usage, 100)
            self.explainer_usage = shap.KernelExplainer(self.model_usage.predict_proba, X_train_summary)


        elif self.model_type == "ada":
            X_train_summary = shap.sample(self.X_train_usage, 100)
            self.explainer_usage = shap.KernelExplainer(self.model_usage.predict_proba, X_train_summary)

        elif self.model_type == "knn":
            X_train_summary = shap.sample(self.X_train_usage, 100)
            self.explainer_usage = shap.KernelExplainer(self.model_usage.predict_proba, X_train_summary)

        elif self.model_type == "random forest":

            self.explainer_usage = shap.TreeExplainer(self.model_usage, self.X_train_usage)

        elif self.model_type == "xgboost":
            self.explainer_usage = shap.TreeExplainer(self.model_usage, self.X_train_usage, model_output='predict_proba')
        else:
            raise InputError("Unknown model type.")


        self.shap_values_usage = self.explainer_usage.shap_values(
            self.X_test_usage)

        feature_names_usage = list(self.X_train_usage.columns.values)

        vals = self.shap_values_usage[1]

        feature_importance_usage = pd.DataFrame(list(zip(feature_names_usage, vals)),
                                                columns=['col_name', 'feature_importance_vals'])
        feature_importance_usage.sort_values(by=['feature_importance_vals'], ascending=False, inplace=True)

        return feature_importance_activity, feature_importance_usage, self.explainer_activity, self.explainer_usage, self.shap_values, self.shap_values_usage, self.X_test_activity, self.X_test_usage

    def explanation_from_feature_importance_activity(self, feature_importance_activity, date, best_hour, diagnostics=False, weather_sel = False):
        self.feature_importance_activity = feature_importance_activity
        self.diagnostics = diagnostics

        sentence = 'We based the recommendation on your past activity and usage of the device. '

        #activity_lags:

        if self.X_test_activity['activity_lag_24'].iloc[self.best_hour] and self.X_test_activity['activity_lag_48'].iloc[self.best_hour] and self.X_test_activity['activity_lag_72'].iloc[self.best_hour] ==0:
            active_past = 'not '
        else:
            active_past = ''

        # input the activity lag with the strongest feature importance
        if feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_24','feature_importance_vals'].to_numpy()[0] >= 0 or \
                feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_48','feature_importance_vals'].to_numpy()[0] >= 0 or \
                feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_72','feature_importance_vals'].to_numpy()[0] >= 0:

                FI_lag = np.argmax([feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_24','feature_importance_vals'],
                                   feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_48','feature_importance_vals'],
                                   feature_importance_activity.loc[feature_importance_activity['col_name']=='activity_lag_72','feature_importance_vals']])

                if FI_lag == 0:
                    activity_lag = 'day'
                elif FI_lag == 1:
                    activity_lag = 'two days'
                elif FI_lag == 2:
                    activity_lag = 'three days'
                else:
                    activity_lag = 'three days'

                part1 = f"We believe you are active today since you were {active_past}active during the last {activity_lag}."
        else:
            part1 = ""

        if weather_sel:
            # weather:
            # need to rewrite that part afterwards, we need different weather data!

            # weather_hourly = pd.read_pickle('../export/weather_unscaled_hourly.pkl')


            d = {'features': ['dwpt', 'rhum', 'temp', 'wdir', 'wspd'],
                 'labels': ['dewing point', 'relative humidity','temperature', 'wind direction', 'windspeed'],
                 'feature_importances' : [feature_importance_activity.loc[feature_importance_activity[
                                                                    'col_name'] == 'dwpt', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_activity.loc[feature_importance_activity[
                                                                    'col_name'] == 'rhum', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_activity.loc[feature_importance_activity[
                                                                    'col_name'] == 'temp', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_activity.loc[feature_importance_activity[
                                                                          'col_name'] == 'wdir', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_activity.loc[feature_importance_activity[
                                                                          'col_name'] == 'wspd', 'feature_importance_vals'].to_numpy()[0]],
                 'feature_values' : [weather_hourly[date].iloc[best_hour, -5:].loc['dwpt'],
                                     weather_hourly[date].iloc[best_hour, -5:].loc['rhum'],
                                     weather_hourly[date].iloc[best_hour, -5:].loc['temp'],
                                     weather_hourly[date].iloc[best_hour, -5:].loc['wdir'],
                                     weather_hourly[date].iloc[best_hour, -5:].loc['wspd']
                                     ]

                 }
            df = pd.DataFrame(data=d)

            sorted_df = df['feature_importances'].sort_values(ascending=False)
            if sorted_df.iloc[0] >= 0:
                weather1_ind = sorted_df.index[0]
                weather1 = df['labels'][weather1_ind]

                value1 = round(df['feature_values'][weather1_ind], 2)

                part2= f"The weather condition ({weather1}:{value1}) support that recommendation."

                if sorted_df.iloc[1] >= 0:

                    weather2_ind = sorted_df.index[1]
                    weather2 = df['labels'][weather2_ind]

                    value2 = round(df['feature_values'][weather2_ind], 2)
                    part2 = f"The weather conditions ({weather1}:{value1}, {weather2}:{value2}) support that recommendation."

            else:
                part2= ""
        else:
            part2 = ""

        # Time features
        # DAY
        day_names = ['day_name_Monday','day_name_Tuesday','day_name_Wednesday','day_name_Thursday','day_name_Saturday','day_name_Sunday']
        for day in day_names:
            if feature_importance_activity.loc[feature_importance_activity['col_name'] == day, 'feature_importance_vals'].to_numpy()[0] >= 0:
                part3 = "The weekday strenghtens that prediction."

                if feature_importance_activity.loc[
                    feature_importance_activity['col_name'] == 'hour', 'feature_importance_vals'].to_numpy()[0] >= 0:
                    part3 = "The weekday and hour strenghtens that prediction."

            else:
                part3 = ""
                if feature_importance_activity.loc[
                    feature_importance_activity['col_name'] == 'hour', 'feature_importance_vals'].to_numpy()[0] >= 0:
                    part3 = "The hour strenghtens that prediction."


        # final activity sentence
        sentence_activity = (str(part1) + str(part2)+ str(part3))

        explanation_sentence = sentence + sentence_activity

        return explanation_sentence

    def explanation_from_feature_importance_usage(self, feature_importance_usage, date, diagnostics=False, weather_sel = False):

        self.feature_importance_usage= feature_importance_usage
        self.diagnostics = diagnostics

        if self.X_test_usage['active_last_2_days'] == 0:
            active_past = 'not'
        else:
            active_past = ''

        if feature_importance_usage.loc[0, 'feature_importance_vals'] >= 0 or feature_importance_usage.loc[1, 'feature_importance_vals'] >= 0:

            FI_lag = np.argmax([feature_importance_usage.loc[0, 'feature_importance_vals'],
                                feature_importance_usage.loc[1, 'feature_importance_vals']])

            if FI_lag == 0:
                device_usage = ""
                number_days = 'day'
            elif FI_lag == 1:
                device_usage = ""
                number_days = 'two days'
            else:
                device_usage = " not"
                number_days = 'two days'

            part1 = f" and have{device_usage} used the device in the last {number_days}"

        else:
            part1= ""

        if weather_sel:
            # weather:
            # need to rewrite that part afterwards, we need different weather data!
            weather_daily = pd.read_pickle('../export/weather_unscaled_daily.pkl')

            d = {'features': ['dwpt', 'rhum', 'temp', 'wdir', 'wspd'],
                 'labels': ['dewing point', 'relative humidity','temperature', 'wind direction', 'windspeed'],
                 'feature_importances' : [feature_importance_usage.loc[feature_importance_usage[
                                                                    'col_name'] == 'dwpt', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_usage.loc[feature_importance_usage[
                                                                    'col_name'] == 'rhum', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_usage.loc[feature_importance_usage[
                                                                    'col_name'] == 'temp', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_usage.loc[feature_importance_usage[
                                                                          'col_name'] == 'wdir', 'feature_importance_vals'].to_numpy()[0],
                                      feature_importance_usage.loc[feature_importance_usage[
                                                                          'col_name'] == 'wspd', 'feature_importance_vals'].to_numpy()[0]],
                 'feature_values': [weather_daily.loc[date].loc['dwpt'],
                                    weather_daily.loc[date].loc['rhum'],
                                    weather_daily.loc[date].loc['temp'],
                                    weather_daily.loc[date].loc['wdir'],
                                    weather_daily.loc[date].loc['wspd']
                 ]


                 }
            df = pd.DataFrame(data=d)

            sorted_df = df['feature_importances'].sort_values(ascending=False)


            if sorted_df.iloc[0] >= 0:
                weather1_ind = sorted_df.index[0]
                weather1 = df['labels'][weather1_ind]

                value1 = round(df['feature_values'][weather1_ind], 2)

                part2= f"The weather condition ({weather1}:{value1}) support that recommendation."

                if sorted_df.iloc[1] >= 0:

                    weather2_ind = sorted_df.index[1]
                    weather2 = df['labels'][weather2_ind]

                    value2 = round(df['feature_values'][weather2_ind], 2)
                    part2 = f"The weather conditions ({weather1}:{value1}, {weather2}:{value2}) support that recommendation."

        else:
            part2 = ""

        sentence_usage = f"We believe you are likely to use the device in the near future since you " \
                         f"were {active_past}active during the last 2 days" + str(part1) + "." + str(part2)
        explanation_sentence = sentence_usage

        return explanation_sentence