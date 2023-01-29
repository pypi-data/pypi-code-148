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



# X_Recommendation Agent
# ===============================================================================================
class X_Recommendation_Agent:
    def __init__(
        self, activity_input, usage_input, load_input, price_input, shiftable_devices, best_hour = None, model_type = 'random forest'):
        self.activity_input = activity_input
        self.usage_input = usage_input
        self.load_input = load_input
        self.price_input = price_input
        self.shiftable_devices = shiftable_devices
        self.model_type = model_type
        self.Activity_Agent = Activity_Agent(activity_input)
        # create dicionnary with Usage_Agent for each device
        self.Usage_Agent = {
            name: Usage_Agent(usage_input, name) for name in shiftable_devices
        }
        self.Load_Agent = Load_Agent(load_input)
        self.Price_Agent = Price_Agent()
        self.best_hour = best_hour

    # calculating costs
    # -------------------------------------------------------------------------------------------
    def electricity_prices_from_start_time(self, date):
        import pandas as pd
        tomorrow = (pd.to_datetime(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d") 

        prices_48 = self.Price_Agent.return_day_ahead_prices(tomorrow)
        prices_from_start_time = pd.DataFrame()
        for i in range(24):
            prices_from_start_time["Price_at_H+" + str(i)] = prices_48.shift(-i)
        # delete last 24 hours
        prices_from_start_time = prices_from_start_time[:-24]
        return prices_from_start_time

    def cost_by_starting_time(self, date, device, evaluation=False):
        import numpy as np
        import pandas as pd

        # get electriciy prices following every device starting hour with previously defined function
        prices = self.electricity_prices_from_start_time(date)
        # build up table with typical load profile repeated for every hour (see Load_Agent)
        if not evaluation:
            device_load = self.Load_Agent.pipeline(
                self.load_input, date, self.shiftable_devices
            ).loc[device]
        else:
            # get device load for one date
            device_load = evaluation["load"][date].loc[device]
        device_load = pd.concat([device_load] * 24, axis=1)
        # multiply both tables and aggregate costs for each starting hour
        costs = np.array(prices) * np.array(device_load)
        costs = np.sum(costs, axis=0)
        costs = costs/1000000
        # return an array of size 24 containing the total cost at each staring hour.
        return costs

    # creating recommendations
    # -------------------------------------------------------------------------------------------
    def recommend_by_device(
        self,
        date,
        device,
        activity_prob_threshold,
        usage_prob_threshold,
        evaluation=False,
        weather_sel=False
    ):
        import numpy as np

        # add split params as input
        # IN PARTICULAR --> Specify date to start training
        split_params = {
            "train_start": "",
            "test_delta": {"days": 1, "seconds": -1},
            "target": "activity",
        }
        # compute costs by launching time:
        costs = self.cost_by_starting_time(date, device, evaluation=evaluation)

        X_train_activity = None
        X_test_activity = None
        model_activity = None
        model_usage = None

        # compute activity probabilities
        if not evaluation:
            if weather_sel:
                activity_probs, X_train_activity, X_test_activity, model_activity = self.Activity_Agent.pipeline_xai(
                    self.activity_input, date, self.model_type, split_params, weather_sel=True)
            else:
                activity_probs, X_train_activity, X_test_activity, model_activity = self.Activity_Agent.pipeline_xai(
                    self.activity_input, date, self.model_type, split_params, weather_sel=False)
        else:
            # get activity probs for date
            activity_probs = evaluation["activity"][date]

        # set values above threshold to 1. Values below to Inf
        # (vector will be multiplied by costs, so that hours of little activity likelihood get cost = Inf)
        activity_probs = np.where(activity_probs >= activity_prob_threshold, 1, float("Inf"))

        # add a flag in case all hours have likelihood smaller than threshold
        no_recommend_flag_activity = 0
        if np.min(activity_probs) == float("Inf"):
            no_recommend_flag_activity = 1

        # compute cheapest hour from likely ones
        self.best_hour = np.argmin(np.array(costs) * np.array(activity_probs))

        # compute likelihood of usage:
        if not evaluation:
            if weather_sel:
                usage_prob, X_train_usage, X_test_usage, model_usage = self.Usage_Agent[device].pipeline_xai(
                    self.usage_input, date,self.model_type, split_params["train_start"], weather_sel=True)
            else:
                usage_prob, X_train_usage, X_test_usage, model_usage = self.Usage_Agent[device].pipeline_xai(
                self.usage_input, date,self.model_type, split_params["train_start"], weather_sel=False)
        else:
            # get usage probs
            name = ("usage_" + device.replace(" ", "_").replace("(", "").replace(")", "").lower())
            usage_prob = evaluation[name][date]


        no_recommend_flag_usage = 0
        if usage_prob < usage_prob_threshold:
            no_recommend_flag_usage = 1

        self.Explainability_Agent = Explainability_Agent(model_activity, X_train_activity, X_test_activity, self.best_hour, model_usage,
        X_train_usage, X_test_usage, model_type=self.model_type)

        explain = Explainability_Agent(model_activity, X_train_activity, X_test_activity,
                                       self.best_hour,model_usage,X_train_usage, X_test_usage,
                                       model_type= self.model_type)
        feature_importance_activity, feature_importance_usage, explainer_activity, explainer_usage, shap_values, shap_values_usage, X_test_activity, X_test_usage = explain.feature_importance()

        tomorrow = (pd.to_datetime(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        return {
            "recommendation_calculation_date": [date],
            "recommendation_date": [tomorrow],
            "device": [device],
            "best_launch_hour": [self.best_hour],
            "no_recommend_flag_activity": [no_recommend_flag_activity],
            "no_recommend_flag_usage": [no_recommend_flag_usage],
            "recommendation": [
                self.best_hour
                if (no_recommend_flag_activity == 0 and no_recommend_flag_usage == 0)
                else np.nan
            ],
            "feature_importance_activity": [feature_importance_activity],
            "feature_importance_usage": [feature_importance_usage],
            "explainer_activity": [explainer_activity],
            "explainer_usage": [explainer_usage],
            "shap_values": [shap_values],
            "shap_values_usage": [shap_values_usage],
            "X_test_activity": [X_test_activity],
            "X_test_usage": [X_test_usage],
        }

    # visualize recommendation_by device
    def visualize_recommendation_by_device(self, dict):
        import datetime
        recommendation_date = str(dict['recommendation_date'][0])
        recommendation_date = datetime.datetime.strptime(recommendation_date, '%Y-%m-%d')
        best_launch_hour = dict['best_launch_hour'][0]
        recommendation_date = recommendation_date.replace(hour=best_launch_hour)
        recommendation_date = recommendation_date.strftime(format = "%d.%m.%Y %H:%M")
        device = dict['device'][0]
        if (dict['no_recommend_flag_activity'][0]== 0 and dict['no_recommend_flag_usage'][0]==0) == True:
            return print('You have one recommendation for the following device: ' + str(device) + '\nPlease use it on ' + recommendation_date[0:10] + ' at '+ recommendation_date[11:]+'.')


    # vizualizing the recommendations
    # -------------------------------------------------------------------------------------------
    def recommendations_on_date_range(
        self, date_range, activity_prob_threshold=0.6, usage_prob_threshold=0.5
    ):
        import pandas as pd

        recommendations = []
        for date in date_range:
            recommendations.append(self.pipeline(date, activity_prob_threshold, usage_prob_threshold))
            output = pd.concat(recommendations)
        return output

    def visualize_recommendations_on_date_range(self, recs):
        import plotly.express as px
        import plotly.graph_objects as go

        fig = go.Figure()

        for device in recs["device"].unique():
            plot_device = recs[recs["device"] == device]
            fig.add_trace(
                go.Scatter(
                    x=plot_device["recommendation_date"],
                    y=plot_device["recommendation"],
                    mode="lines",
                    name=device,
                )
            )
        fig.show()

    def histogram_recommendation_hour(self, recs):
        import seaborn as sns

        ax = sns.displot(recs, x="recommendation", binwidth=1)
        ax.set(xlabel="Hour of Recommendation", ylabel="counts")

    # pipeline function: create recommendations
    # -------------------------------------------------------------------------------------------
    def pipeline(self, date, activity_prob_threshold, usage_prob_threshold, evaluation=False, weather_sel=False):
        import pandas as pd

        recommendations_by_device = self.recommend_by_device(
            date,
            self.shiftable_devices[0],
            activity_prob_threshold,
            usage_prob_threshold,
            evaluation=evaluation,
        )
        recommendations_table = pd.DataFrame.from_dict(recommendations_by_device)

        for device in self.shiftable_devices[1:]:
            if weather_sel:
                recommendations_by_device = self.recommend_by_device(
                    date,
                    device,
                    activity_prob_threshold,
                    usage_prob_threshold,
                    evaluation=evaluation,
                    weather_sel=True
                )
            else:
                recommendations_by_device = self.recommend_by_device(
                    date,
                    device,
                    activity_prob_threshold,
                    usage_prob_threshold,
                    evaluation=evaluation,
                )
            recommendations_table = recommendations_table.append(
                pd.DataFrame.from_dict(recommendations_by_device)
            )
            recommendations_table["index"] = recommendations_table.apply(lambda row: row.recommendation_date + "_" + row.device, axis=1)
            recommendations_table.set_index("index", inplace = True)
        return recommendations_table

    def visualize_recommendation(self, recommendations_table, price, diagnostics=False):
        self.diagnostics = diagnostics
        from datetime import datetime
        import shap

        for r in range(len(recommendations_table)):
            if (recommendations_table.no_recommend_flag_activity.iloc[r] == 0 and
                recommendations_table.no_recommend_flag_usage.iloc[r] == 0) == True:

                recommendations = True
            else:
                recommendations = False

        if recommendations == True:

            feature_importance_activity = recommendations_table['feature_importance_activity'].iloc[0]
            date = recommendations_table.recommendation_date.iloc[0]
            best_hour = recommendations_table.best_launch_hour.iloc[0]
            explaination_activity = Explainability_Agent_i.explanation_from_feature_importance_activity(feature_importance_activity, date=date , best_hour=best_hour, diagnostics=self.diagnostics)

            output = []
            explaination_usage = []
            for i in range(len(recommendations_table)):

                if (recommendations_table.no_recommend_flag_activity.iloc[i] == 0 and
                recommendations_table.no_recommend_flag_usage.iloc[i] == 0) == True:

                    date_and_time = recommendations_table.recommendation_date.iloc[i] + ':' + str(recommendations_table.best_launch_hour.iloc[i])

                    date_and_time =  datetime.strptime(date_and_time, '%Y-%m-%d:%H')

                    date_and_time_show = date_and_time.strftime(format = "%d.%m.%Y %H:%M")
                    date_and_time_price = date_and_time.strftime(format = "%Y-%m-%d %H:%M:%S")

                    price_rec = price.filter(like=date_and_time_price, axis=0)['Price_at_H+0'].iloc[0]
                    price_mean = price['Price_at_H+0'].sum() / 24
                    price_dif = price_rec / price_mean
                    price_savings_percentage = round((1 - price_dif) * 100, 2)

                    output = print('You have a recommendation for the following device: ' + recommendations_table.device.iloc[i] + '\n\nPlease use the device on the ' + date_and_time_show[0:10] + ' at ' + date_and_time_show[11:] + " o'clock because it saves you " + str(price_savings_percentage) + ' % of costs compared to the mean of the day.\n')
                    feature_importance_usage_device = recommendations_table['feature_importance_usage'].iloc[i]
                    explaination_usage = Explainability_Agent_i.explanation_from_feature_importance_usage(feature_importance_usage_device, date=date, diagnostics=self.diagnostics)
                    print(explaination_usage)


                    if self.diagnostics == True:
                        print('Vizualizations for further insights into our predictions: ')
                        explainer_usage = recommendations_table['explainer_usage'].iloc[i]
                        shap_values_usage = recommendations_table['shap_values_usage'].iloc[i]
                        X_test_usage = recommendations_table['X_test_usage'].iloc[i]
                        shap_plot_usage = shap.force_plot(explainer_usage.expected_value[1], shap_values_usage[1], X_test_usage)
                        display(shap_plot_usage)

                else:
                    print('There is no recommendation for the device ' + recommendations_table.device.iloc[i] + ' .')

            print(explaination_activity)

            if self.diagnostics == False:
                print('For detailed information switch on the diagnostics parameter.')
            return

        else:
            print('There are no recommendations for today.')
            return None            