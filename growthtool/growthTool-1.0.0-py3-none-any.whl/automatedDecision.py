import operator

import numpy as np
import datetime
import copy

import pandas as pd
from scipy import stats
from shapely.geometry import Polygon, Point

import API
import queries
import settings
from blockInfo import Block, Analysis, Result


class automatedDecision(object):
    def __init__(self, id_plot, mode):
        print('Start growth tool automation')
        self.API_manager = API.Manager()
        self.API_manager.set_manual_block(id_plot)
        # get & set block info,measurements data(std_cleaner)
        self.blockObject = Block(id=id_plot, manual=True)
        self.info = self.API_manager.get_info()
        self.operation_mode = mode
        # self.plot_poly= queries.get_plot_coordinates(id_plot)['plot_coordinates'][0][0]
        self.update_models()
        result, done, red_flag = self.run_auto()
        print(result, done, red_flag)

    def validate_sample(self):
        samples = self.blockObject.get_block_info()['distribution_info']['diameter']
        smoothed_samples = samples.rolling(2).mean().rolling(2).mean().dropna()
        if len(samples) <= 150:
            print('Not enough samples')
            self.blockObject.set_red_flag(True)
            raise Exception
        else:
            try:
                shapiro_test = stats.shapiro(samples)
                mean = smoothed_samples.mean()
                if shapiro_test[1] < 0.05:
                    # comes from normal dist
                    self.blockObject.set_stat_type('mean')
                    self.blockObject.set_size_value()
                else:
                    print('Error: validate sample failed')
            except Exception as e:
                print(str(e))

    def run_auto(self, model_id=None):
        try:
            if self.operation_mode == settings.config["operationMode"]["regular"] or self.operation_mode == \
                    settings.config["operationMode"]["change_date"]:
                self.validate_sample()
                first_step_models_res = self.get_models_first_step()
                size_normaliztion_models, date_normaliztion_models = self.define_models_params(first_step_models_res)
                second_step_models_res = self.get_models_second_step(size_normaliztion_models, date_normaliztion_models)
                self.top1_model = self.get_models_third_step(second_step_models_res)[0][0]
            elif self.operation_mode == settings.config["operationMode"]["force_model"]:
                self.top1_model = self.force_model(model_id)
            elif self.operation_mode == settings.config["operationMode"]["change_packout_metadata"]:
                # Do just distribution at picking re-calc in case we change the packout metadata.
                pass

            if self.top1_model is not None:
                self.distribution_analysis(self.top1_model)
                self.blockObject.set_top_1_model(copy.deepcopy(self.top1_model))
                result = Result(self.blockObject)
                result.set_weights()
                result.save_samples(path_local=False)
                result.save_dist()
                res = result.id
                done = True
            else:
                res = None
                done = None
        except Exception as e:
            print('Failed to run auto, ', e)
            self.blockObject.set_red_flag(True)
            res = None
            done = False
        finally:
            redFlag = self.blockObject.get_red_flag()
            return res, done, redFlag

    def force_model(self, model_name):
        print('force model id = ', model_name)

        relevant_model = [model for model in settings.models_objects if model.model_id == model_name][0]

        block_info = self.blockObject.get_block_info()
        relevant_model.set_dynamic_variables(info=block_info)
        _, day_opt2 = relevant_model.adjust(method='by_size')
        diff_day_opt2 = relevant_model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2)
        if day_opt2 is not None:
            if abs(diff_day_opt2) <= 10:
                relevant_model.set_dynamic_variables(days=day_opt2, calc_delta_size=True, diff_days=diff_day_opt2)

        if self.blockObject.get_scan_num() == 2:
            _, day_opt1 = relevant_model.adjust(method='by_date', first_day=block_info['scans']['1st']['date'])
            if day_opt1 is not None:
                relevant_model.set_dynamic_variables(days=day_opt1, calc_delta_size=True,
                                                     diff_days=relevant_model.find_fixed_day(
                                                         block_info['scans']['1st']['date'],
                                                         delta=day_opt1))

        relevant_model.set_dynamic_variables(calc_delta_size=True)

        return relevant_model

    def get_models_first_step(self):
        """
        This function filters models with suitable fruit type & picking period
        :return:list of models is filtered according to the specified parameters
        """
        self.analysis = Analysis(self.blockObject)
        models = self.analysis.match_models()
        print('models lens =', len(models))
        return models

    def get_models_second_step(self, size_normaliztion_models, date_normaliztion_models):
        """
        This function creates 2 sorted separate list according to calculate_distance function's delta results and pass those lists to check_growth_rate function


        :param size_normaliztion_models: list of models
        :param date_normaliztion_models: list of models
        :return: list of tuples -[model , model's picking size(acoording to models_value_list)]
        """

        sorted_size_list = {}
        sorted_date_list = {}
        models_value_list = {}

        for model in size_normaliztion_models:
            analysis_point, x_model, y_model, formula, labels, x_scans, y_scans = self.API_manager.parser_model(
                model=model)

            try:
                if self.blockObject.get_scan_num() == 1:
                    test_date = list((x_scans[len(x_scans) - 1], y_scans[len(y_scans) - 1]))
                    min_delta = self.calculate_distance(y_model, x_model, test_date)
                    sorted_size_list[model] = min_delta
                    models_value_list[model] = labels['model_value']

                else:
                    first_test_date = list((x_scans[len(x_scans) - 2], y_scans[len(y_scans) - 2]))
                    second_test_date = list((x_scans[len(x_scans) - 1], y_scans[len(y_scans) - 1]))

                    first_min_delta = self.calculate_distance(y_model, x_model, first_test_date)
                    second_min_delta = self.calculate_distance(y_model, x_model, second_test_date)
                    min_delta = (first_min_delta + second_min_delta) / 2
                    sorted_size_list[model] = min_delta
                    models_value_list[model] = labels['model_value']

            except Exception as e:
                print('Cannot calculate scan delta from model ', model.model_id, ' error is: ', str(e))

        for model in date_normaliztion_models:
            analysis_point, x_model, y_model, formula, labels, x_scans, y_scans = self.API_manager.parser_model(
                model=model)
            try:
                if self.blockObject.get_scan_num() == 1:
                    test_date = list((x_scans[len(x_scans) - 1], y_scans[len(y_scans) - 1]))
                    min_delta = self.calculate_distance(y_model, x_model, test_date)
                    # sorted_models_list.append([model.model_id,min_delta])
                    sorted_date_list[model] = min_delta
                    models_value_list[model] = labels['model_value']

                else:
                    first_test_date = list((x_scans[len(x_scans) - 2], y_scans[len(y_scans) - 2]))
                    second_test_date = list((x_scans[len(x_scans) - 1], y_scans[len(y_scans) - 1]))

                    first_min_delta = self.calculate_distance(y_model, x_model, first_test_date)
                    second_min_delta = self.calculate_distance(y_model, x_model, second_test_date)
                    min_delta = (first_min_delta + second_min_delta) / 2
                    # sorted_models_list.append([model.model_id,min_delta])
                    sorted_date_list[model] = min_delta
                    models_value_list[model] = labels['model_value']

            except Exception as e:
                print('Cannot calculate scan delta from model ', model.model_id, ' error is: ', str(e))

        sorted_size = sorted(sorted_size_list.items(), key=operator.itemgetter(1))
        sorted_date = sorted(sorted_date_list.items(), key=operator.itemgetter(1))

        print('_______________by size______________')
        for model in sorted_size:
            print('model name = ', model[0].model_id, ' has delta of ', model[1])

        print('_______________by date______________')
        for model in sorted_date:
            print('model name = ', model[0].model_id, ' has delta of ', model[1])

        print('_______________growth rate data______________')
        self.check_growth_rate(sorted_size, sorted_date, x_scans, y_scans, models_value_list)
        top_models = sorted(self.top_models.items(), key=operator.itemgetter(1))

        print('_______________top models______________')
        for model in top_models:
            print('model name = ', model[0].model_id, ' has model value of ', model[1])

        return top_models

    def get_models_third_step(self, top_models):
        """

        :param top_models: list of models
        :return:  single model whose fruit size is closest to the average size
        """
        # TODO: add climate filter-depends on giving each model area a coordinates to compare with block polygon
        # coordinates = []
        # for point in self.plot_poly:
        #     coordinates.append((point['x'], point['y']))
        # print(coordinates)
        # curr_polygon = Polygon(coordinates)
        #
        #
        #
        # climate_data=settings.climate_data
        # print('start check climate area')
        # for area in climate_data['coordinate']:
        #     if type(area)==str:
        #         print(area.split(',')[0],area.split(',')[1])
        #         curr_point= Point(float(area.split(',')[0]),float(area.split(',')[1]))
        #         test_point=Point(36.46824388200002, -119.184151443)
        #         if curr_polygon.contains(test_point):
        #             print('found')

        top1_model = self.predicted_size_avg_filter(top_models)
        return top1_model

    def check_growth_rate(self, by_size_list, by_date_list, x_scans, y_scans, models_value_list):
        """
        This function iterate all models in by_size_list & by_date_list and define their growth rate between different pairs of time points.
        The loop will end when find max_model_num models that have valid growth rate, and return those top models.

        Scenarios:
        1. Block has one scan only - check growth rate between 1st-DORG (according to fruit type)
        2.Block has two scans - check growth rate between 1st-2nd and if valid check growth rate between 1st-DORG (according to fruit type)

        Models included in by_size_list have priority, therefore there are two loops for each scenario

        :param by_size_list: sorted list of tuples- [model,delta]
        :param by_date_list: sorted list of tuples- [model,delta]
        :param x_scans: list of floats that represent dates
        :param y_scans: list of floats that represent sizes
        :param models_value_list: list of tuples- [model, model's picking size]

        """
        fruit_type = self.blockObject.block_info['fruit_type']
        max_model_num = settings.config["automationConsts"]["max_model_num"]
        orange_growth_const = float(settings.config["automationConsts"]["orange"])
        mandarin_growth_const = float(settings.config["automationConsts"]["mandarin"])
        first_date = self.blockObject.block_info['scans']['1st']['date']
        second_date = self.blockObject.block_info['scans']['2nd']['date']
        self.top_models = {}
        self.growth_rate_data = []

        for m in by_size_list:
            if len(self.top_models) < max_model_num:
                if self.blockObject.get_scan_num() == 1:
                    first_size = y_scans[len(y_scans) - 1]
                    picking_date = self.get_calendar_point(m[0].start_date, m[0].dynamic_variables['1st']['day'] +
                                                           m[0].dynamic_variables['delta_2nd']['day'] +
                                                           m[0].dynamic_variables['delta_picking']['day'])
                    picking_size = models_value_list.get(m[0])
                    if fruit_type == "Mandarin":
                        rg_date = datetime.datetime(first_date.year, 12, 15)

                        self.get_gr(relevant_date=first_date, first_size=first_size, picking_date=picking_date,
                                    picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                    multi_factor=mandarin_growth_const,
                                    model=m, scan_num=self.blockObject.get_scan_num())
                    if fruit_type == "Orange":
                        rg_date = datetime.datetime(first_date.date().year, 11, 13)

                        self.get_gr(relevant_date=first_date, first_size=first_size, picking_date=picking_date,
                                    picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                    multi_factor=orange_growth_const,
                                    model=m, scan_num=self.blockObject.get_scan_num())

                else:
                    # calc growth rate from 1st to 2nd
                    first_growth_rate = abs((y_scans[len(y_scans) - 1]) - (y_scans[len(y_scans) - 2])) / abs(
                        (x_scans[len(x_scans) - 1]) - (x_scans[len(x_scans) - 2]))

                    if not self.is_valid_gr(first_growth_rate, fruit_type, 2, first_date.month, second_date.month):
                        print('gr 1st-2nd: model ', m[0].model_id, ' has unvalid gr of ', first_growth_rate)

                    else:
                        first_size = y_scans[len(y_scans) - 1]
                        picking_date = self.get_calendar_point(m[0].start_date, m[0].dynamic_variables['1st']['day'] +
                                                               m[0].dynamic_variables['delta_2nd']['day'] +
                                                               m[0].dynamic_variables['delta_picking']['day'])
                        picking_size = models_value_list.get(m[0])

                        if fruit_type == "Mandarin":
                            rg_date = datetime.datetime(second_date.year, 12, 15)

                            self.get_gr(relevant_date=second_date, first_size=first_size, picking_date=picking_date,
                                        picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                        multi_factor=mandarin_growth_const,
                                        model=m, scan_num=self.blockObject.get_scan_num())

                        if fruit_type == "Orange":
                            rg_date = datetime.datetime(second_date.year, 11, 13)

                            self.get_gr(relevant_date=second_date, first_size=first_size, picking_date=picking_date,
                                        picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                        multi_factor=orange_growth_const,
                                        model=m, scan_num=self.blockObject.get_scan_num())

        for m in by_date_list:
            if len(self.top_models) < max_model_num:
                if self.blockObject.get_scan_num() == 1:
                    first_size = y_scans[len(y_scans) - 1]
                    picking_date = self.get_calendar_point(m[0].start_date, m[0].dynamic_variables['1st']['day'] +
                                                           m[0].dynamic_variables['delta_2nd']['day'] +
                                                           m[0].dynamic_variables['delta_picking']['day'])
                    picking_size = models_value_list.get(m[0])
                    if fruit_type == "Mandarin":
                        rg_date = datetime.datetime(first_date.year, 12, 15)

                        self.get_gr(relevant_date=first_date, first_size=first_size, picking_date=picking_date,
                                    picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                    multi_factor=mandarin_growth_const,
                                    model=m, scan_num=self.blockObject.get_scan_num())

                    if fruit_type == "Orange":
                        rg_date = datetime.datetime(first_date.year, 11, 13)

                        self.get_gr(relevant_date=first_date, first_size=first_size, picking_date=picking_date,
                                    picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                    multi_factor=orange_growth_const,
                                    model=m, scan_num=self.blockObject.get_scan_num())

                else:
                    # calc growth rate from 1st to 2nd
                    first_growth_rate = abs((y_scans[len(y_scans) - 1]) - (y_scans[len(y_scans) - 2])) / abs(
                        (x_scans[len(x_scans) - 1]) - (x_scans[len(x_scans) - 2]))
                    if not self.is_valid_gr(first_growth_rate, fruit_type, 2, first_date.month, second_date.month):
                        print('gr 1st-2nd: model ', m[0].model_id, ' has unvalid gr of ', first_growth_rate)

                    else:
                        first_size = y_scans[len(y_scans) - 1]
                        picking_date = self.get_calendar_point(m[0].start_date, m[0].dynamic_variables['1st']['day'] +
                                                               m[0].dynamic_variables['delta_2nd']['day'] +
                                                               m[0].dynamic_variables['delta_picking']['day'])
                        picking_size = models_value_list.get(m[0])

                        if fruit_type == "Mandarin":
                            rg_date = datetime.datetime(second_date.year, 12, 15)

                            self.get_gr(relevant_date=second_date, first_size=first_size, picking_date=picking_date,
                                        picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                        multi_factor=mandarin_growth_const,
                                        model=m, scan_num=self.blockObject.get_scan_num())
                            # growth_rate_data.append([m[0].model_id, m[1], first_growth_rate, growth_rate, rg_size])

                        if fruit_type == "Orange":
                            rg_date = datetime.datetime(second_date.year, 11, 13)

                            self.get_gr(relevant_date=second_date, first_size=first_size, picking_date=picking_date,
                                        picking_size=picking_size, fruit_type=fruit_type, rg_date=rg_date,
                                        multi_factor=orange_growth_const,
                                        model=m, scan_num=self.blockObject.get_scan_num())

        df = pd.DataFrame(self.growth_rate_data)
        df.to_csv(
            r'C:\Users\NoySartori\fruitspec projects\growth tool\automated decision\run result\growth_rate_res.csv')

    def get_gr(self, relevant_date, first_size, picking_date,
               picking_size, fruit_type, rg_date, multi_factor, model, scan_num):
        """

        This function calculate the growth rate according to adjust scan_num,fruit_type and given points
        """
        diff_day = abs((picking_date - rg_date).days)
        rg_size = picking_size - (multi_factor * diff_day)
        growth_rate = abs(rg_size - first_size) / abs((rg_date.date() - relevant_date).days)
        self.growth_rate_data.append([model[0].model_id, model[1], growth_rate, rg_size])
        if self.is_valid_gr(growth_rate, fruit_type, scan_num, relevant_date.month, rg_date.month):
            self.top_models[model[0]] = picking_size
            print('Model ', model[0].model_id, ' insert to top 5 models and has model value of ',
                  picking_size)
        else:
            self.blockObject.set_red_flag(True)

    def is_valid_gr(self, gr, fruit_type, scan_num, from_date, to_date):
        gr_data = settings.fruit_gr
        if scan_num == 1:
            rslt_df = gr_data[(gr_data['fruit_type'] == fruit_type) & (gr_data['scan_num'] == scan_num) & (
                    gr_data['scan_date_from'] == from_date)]
        else:
            rslt_df = gr_data[(gr_data['fruit_type'] == fruit_type) & (gr_data['scan_num'] == scan_num) & (
                    gr_data['scan_date_from'] == from_date) & (gr_data['scan_date_to'] == to_date)]

        return ((gr > rslt_df['min'].item()) and (gr < rslt_df['max'].item()))

    def distribution_analysis(self, model):
        info = self.blockObject.get_block_info()['distribution_info']['caliber_at_picking']
        dropped_ratio = self.blockObject.get_dropped(self.blockObject.get_samples(obj=model)['picking_time'])
        if dropped_ratio > 0.2:
            # raise Exception('More than 20% samples were dropped')
            print('More than 20% samples were dropped')
            self.blockObject.set_red_flag(True)
        if info['history_carton'] is not None:
            if not Analysis.compare_distributions(info['history_carton'], info['current_carton']):
                # raise Exception('History packout points on more than 1 bin count in peak difference')
                print('History packout points on more than 1 bin count in peak difference')
                self.blockObject.set_red_flag(True)

    def predicted_size_avg_filter(self, models):

        if len(models) > 0:
            second_values = [x[1] for x in models]
            avg_fruit_size = sum(second_values) / len(models)
            print('avg of models value = ', avg_fruit_size)
            min_diff = min(second_values, key=lambda x: abs(x - (avg_fruit_size)))
            final_model = [item for item in models if item[1] == min_diff]
            print('final model is ', final_model[0][0].model_id)
            return final_model
        return None

    def define_models_params(self, models):
        """
        This function defines the parameters for each model.

        :param models: List of ModelObject
        :return: two separate lists according to normalization type
        """
        block_info = self.blockObject.get_block_info()
        size_normaliztion_models = []
        date_normaliztion_models = []
        for model in models:

            model.set_dynamic_variables(info=block_info)
            _, day_opt2 = model.adjust(method='by_size')
            diff_day_opt2 = model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2)
            if day_opt2 is not None:
                if abs(diff_day_opt2) <= 10:
                    model.set_dynamic_variables(days=day_opt2, calc_delta_size=True, diff_days=diff_day_opt2)
                    size_normaliztion_models.append(model)
                    continue

            if self.blockObject.get_scan_num() == 2:
                _, day_opt1 = model.adjust(method='by_date', first_day=block_info['scans']['1st']['date'])
                if day_opt1 is not None:
                    model.set_dynamic_variables(days=day_opt1, calc_delta_size=True,
                                                diff_days=model.find_fixed_day(block_info['scans']['1st']['date'],
                                                                               delta=day_opt1))
                    date_normaliztion_models.append(model)
                    continue

            model.set_dynamic_variables(calc_delta_size=True)
            date_normaliztion_models.append(model)

        return size_normaliztion_models, date_normaliztion_models

    def calculate_distance(self, samples, dates, point):
        """
        The function searches for the optimal point to calculate the minimum delta in its range.
        :param samples: sizes values of model
        :param dates: dates values of model
        :param point: [date,size]
        :return: minimal delta between point to model
        """

        dates = np.array(dates)
        samples = np.array(samples)
        diff = dates - point[0]
        date_id = np.argmin(np.abs(diff))
        date_diff = diff[date_id]
        if date_diff > 0:

            try:
                vec = np.arange(samples[date_id - 1], samples[date_id],
                                abs(samples[date_id] - samples[date_id - 1]) / np.abs(
                                    dates[date_id - 1] - dates[date_id]))
            except:
                vec = np.arange((samples[date_id]), (samples[date_id + 1]),
                                abs(np.abs((samples[date_id]) - (samples[date_id + 1])) / np.abs(
                                    dates[date_id] - dates[date_id + 1])))
        else:

            try:
                vec = np.arange((samples[date_id]), (samples[date_id + 1]),
                                abs(np.abs((samples[date_id]) - (samples[date_id + 1])) / np.abs(
                                    dates[date_id] - dates[date_id + 1])))
            except:
                vec = np.arange((samples[date_id - 1]), (samples[date_id]),
                                abs(np.abs((samples[date_id - 1]) - (samples[date_id])) / np.abs(
                                    dates[date_id - 1] - dates[date_id])))
            # vec = np.arange((samples[date_id]), (samples[date_id + 1]),abs((samples[date_id]) - (samples[date_id + 1]) / np.abs(dates[date_id] - dates[date_id + 1])))
        distance = abs(vec[int(date_diff)] - point[1])

        return distance

    def get_calendar_point(self, start_date, int_day, string=False):
        date = start_date + datetime.timedelta(days=int_day)
        # in case of using for calc
        if string == False:
            return date
        # in case of using for UI display
        elif string == True:
            display_date = date.strftime("%d/%m")
            return display_date

    def update_models(self):
        self.API_manager.update_models()


if __name__ == '__main__':
    obj = automatedDecision(6467, 1)
    #12557
    #6467 - OG PLOT
    # 7244
    # 6023
