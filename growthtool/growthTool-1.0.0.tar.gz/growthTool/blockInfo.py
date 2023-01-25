import os
from os.path import join
from os import mkdir
import math
from boto3 import resource
from botocore.exceptions import ClientError
from pandas import read_csv, DataFrame, IntervalIndex, concat, cut, isna
from datetime import datetime, timedelta
from math import inf as inf_math
from glob import glob
from scipy import stats
import copy

import queries
import settings
from ModelObject import ModelObject
from numpy import nansum, arange, isnan, mean, around, array as array_np, argmin
from os import path
from MplCanvas import sizeDistribution
import logging

from STDCleaner import STDCleaner


class Block():

    def __init__(self, id, manual=False, logger=None):
        self.logger = logger if logger is not None else logging.getLogger(str(id))
        self.init_block_info_struct()
        self.stat_type = None
        self.top_1_model = None
        self.scan_num = None
        self.red_flag = False
        self.is_manual=True

        metadata = queries.get_init_block(id).iloc[0]
        plot_id = int(metadata.loc['plot_id'])
        season = int(metadata.loc['project_season'])
        scan_date = metadata['project_plot_scan_date']
        self.scans = queries.get_scans(plot_id, season, scan_date)

        # desc order by scan date
        self.set_scans(metadata)

        if manual is False:
            if not self.find_results():
                self.check_automation_limitation(queries.get_fruit_type(int(metadata.loc['plot_fruit_type'])))
                self.read_metadata(metadata, self.scans.iloc[0])
        else:
            self.read_metadata(metadata, self.scans.iloc[0])

    def init_block_info_struct(self):
        self.block_info = {'customer_name': '',
                           'country': '',
                           'block_name': '',
                           'fruit_type': '',
                           'fruit_variety': '',
                           'soil_type': '',
                           'planting_year': '',
                           'rootstock': '',
                           'existed result': None,
                           'scans': {},
                           'picking_date': None,
                           'distribution_info': {'box_W': [], 'diameter': [], 'std': None, 'mean': None, 'mode': None, 'median': None,
                                                 'caliber_at_picking': {'interval_size': None, 'history_carton': None, 'current_carton': None, 'labels': None, 'box_count': None,
                                                                        'coef_caliber_unit': 1,
                                                                        'coef_weight_unit': 1, 'weight_per_box': None},
                                                 'size_at_picking': {'interval_size': None, 'interval_size_labels': None}},
                           'path_local': {'input': None, 'output': None}}

    def read_metadata(self, metadata, packout_metadata_df):
        self.block_info['block_name'] = metadata.loc['plot_code']
        self.block_info['planting_year'] = str(metadata.loc['plot_planting_year'])
        self.block_info['customer_name'] = queries.get_customer_info(int(metadata.loc['customer_id']), col='customer_code')
        self.block_info['country'] = queries.get_customer_info(int(metadata.loc['customer_id']), col='customer_country')
        self.block_info['hemisphere'] = settings.countries[settings.countries["country"].str.contains(self.block_info['country'].lower())]['hemisphere'].iloc[0]
        self.block_info['fruit_type'] = queries.get_fruit_type(int(metadata.loc['plot_fruit_type']))
        self.block_info['fruit_variety'] = queries.get_fruit_variety(int(metadata.loc['plot_fruit_variety']))
        self.block_info['soil_type'] = queries.get_soil_type(int(metadata.loc['plot_soil']))
        self.block_info['rootstock'] = queries.get_rootstock_type(int(metadata.loc['plot_root_stock']))

        self.set_packout_info(packout_metadata_df)
        self.set_local_path(code=metadata.loc['plot_code'])
        self.set_picking_date(date=metadata["AssumedPickingTime"])
        self.set_historical_packout(season=int(metadata.loc['project_season']), current_packing_method=metadata['Packing_method'])

    def set_scans(self, metadata):
        self.scan_num = 2 if len(self.scans) > 1 else 1
        # ensure that ['scans']['2nd'] exist
        if self.scan_num == 1:
            DICT = {'2nd':
                        {'main': None,
                         'bucket': None,
                         'date': None,
                         'input_s3': None,
                         'output_s3': None,
                         'small': None,
                         'medium': None,
                         'large': None,
                         'std': None,
                         'mean': None,
                         'median': None,
                         'mode': None,
                         'diameter': None}}

            self.block_info['scans'].update(DICT)

        # default last 2 scans or last one scan
        for i, row in self.scans.iterrows():
            main = False
            if i == 0:
                if self.scan_num == 1:
                    main = True
                    num = "1st"
                else:
                    main = True
                    num = "2nd"
            elif i == 1:
                num = "1st"
            else:
                num = str(i)

            date = datetime.strptime(self.scans['project_plot_scan_date'].iloc[i], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            scan_date_s3 = str(date.day).zfill(2) + str(date.month).zfill(2) + str(date.year)[2:]
            project_code = self.scans['project_code'].iloc[i]

            DICT = {num:{'main': None,
                         'bucket': None,
                         'date': None,
                         'input_s3': None,
                         'output_s3': None,
                         'small': None,
                         'medium': None,
                         'large': None,
                         'std': None,
                         'mean': None,
                         'median': None,
                         'mode': None,
                         'diameter': None}}

            # YS & SIZE ONLY
            if row['project_type'] == 1 or row['project_type'] == 2:
                DICT[num]['main'] = main
                DICT[num]['bucket'] = settings.config["AWS"]["YS_bucket"]
                DICT[num]['date'] = date
                DICT[num]['input_s3'] = '{0}/{1}/{2}/{3}/{4}/{5}'.format('input', metadata.loc['customer_code'], scan_date_s3,
                                                                                             project_code, metadata.loc['plot_code'],
                                                                                             'measurements.csv')

                DICT[num]['output_s3'] = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}'.format('output', metadata.loc['customer_code'], scan_date_s3,
                                                                                                      project_code, metadata.loc['plot_code'], "Results", "Size", metadata.loc['plot_code'] + '.csv')
            # CALIPER
            else:
                DICT[num]['main'] = main
                DICT[num]['bucket'] = settings.config["AWS"]["caliper_bucket"]
                DICT[num]['date'] = date
                DICT[num]['input_s3'] = '{0}/{1}/{2}/{3}'.format(metadata.loc['customer_code'], project_code,
                                                                                             metadata.loc['plot_code'],
                                                                                             f'measurements_{scan_date_s3}.csv')

                DICT[num]['output_s3'] = '{0}/{1}/{2}/{3}'.format(metadata.loc['customer_code'], project_code,
                                                                                                      metadata.loc['plot_code'],
                                                                          f'{metadata.loc["plot_code"]}.csv')

            self.block_info['scans'].update(DICT)
            self.set_samples(num, metadata['plot_code'], main=main)

    def set_local_path(self, code):
        # make folder according to block name code
        self.block_info['path_local']['output'] = join('output', code)
        if path.isdir(self.block_info['path_local']['output']) is False:
            mkdir(self.block_info['path_local']['output'])

    def set_picking_date(self, date):

        # finding picking year according to scan year and the month of picking
        refer_date = self.block_info['scans']['2nd']['date'] if self.block_info['scans']['2nd']['date'] is not None else self.block_info['scans']['1st']['date']
        if self.block_info['scans']['1st']['date'] == None:
            raise ValueError("There is no scan date in portal")
        if date is None:
            res_date=queries.get_picking_date_by_fruit_variety(self.block_info['fruit_variety'])
            self.block_info['picking_date'] = Block.datime_picking_date(res_date, refer_date)
        else:
            self.block_info['picking_date'] = Block.datime_picking_date(date, refer_date)


    @staticmethod
    def datime_picking_date(date, refer_date):
        day = settings.config["periodTime"][date.split(" ")[0]]
        month = date.split(" ")[1]
        year = refer_date.year if refer_date.month - datetime.strptime(month, '%B').month <= 0 else refer_date.year + 1
        s = "{0} {1}, {2}".format(str(day), month, str(year))
        picking_date = datetime.strptime(s, '%d %B, %Y').date()
        return picking_date

    # measurements from s3
    def set_samples(self, num, code, main):
        # download csv from input dir in S3 id exist
        dir_csv = join('input', f"{code}_{num}.csv")
        _resource = resource('s3', aws_access_key_id=settings.config["AWS"]["access key"], aws_secret_access_key=settings.config["AWS"]["secret key"])
        try:
            _resource.meta.client.download_file(self.block_info['scans'][num]['bucket'], self.block_info['scans'][num]['input_s3'], dir_csv)
        except ClientError:
            pass

        # check existence of csv for the block
        if not glob(dir_csv):
            raise FileExistsError('measurement CSV have not been found')

        csv_data = read_csv(dir_csv)
        os.remove(dir_csv)
        #Check if manual or caliper file
        if(csv_data.shape[1]>1):
            if(csv_data.columns[0] == ("diameter") and csv_data.columns[1]==("count") and csv_data.columns[2]==("std")):
                csv_data=STDCleaner.clean_std(csv_data)
                self.is_manual=False
        samples = csv_data['diameter'].sort_values(ascending=True).dropna(axis=0).reset_index(drop=True)
        if samples.empty:
            raise Exception('diameter column is empty, please check csv. file')
        try:
            # for UI needs
            if self.is_manual:
                self.block_info['scans'][num]['medium'] = round(samples.mean(), 2)
                self.block_info['scans'][num]['mean'] = samples.mean()
                self.block_info['scans'][num]['median'] = samples.median()
            else :
                self.block_info['scans'][num]['medium'] = samples.median()
                self.block_info['scans'][num]['mean'] = samples.median()
                self.block_info['scans'][num]['median'] = samples.median()

            self.block_info['scans'][num]['small'] = round(samples.min(), 2)
            self.block_info['scans'][num]['large'] = round(samples.max(), 2)
            self.block_info['scans'][num]['std'] = samples.std()
            self.block_info['scans'][num]['mode'] = Analysis.choose_mode(samples)
            self.block_info['scans'][num]['diameter'] = samples



            if main == True:
                self.set_main_scan(num)

        except TypeError:
            raise TypeError('error occurred while reading diameter column, please check csv. file')

    def set_main_scan(self, num):
        # for analysis needs + UI needs
        self.block_info['distribution_info']['diameter'] = self.block_info['scans'][num]['diameter']
        # UI needs only
        self.block_info['distribution_info']['std'] = self.block_info['scans'][num]['std']
        self.block_info['distribution_info']['mean'] = self.block_info['scans'][num]['mean']
        self.block_info['distribution_info']['median'] = self.block_info['scans'][num]['median']
        self.block_info['distribution_info']['mode'] = self.block_info['scans'][num]['mode']

    def set_packout_info(self, df):
        # check the content of the constraint record - exist and contains values
        try:
            caliber_row = df.to_frame().transpose()
            self.block_info['distribution_info']['caliber_at_picking']['box_count'] = \
                caliber_row[[col for col in caliber_row.columns if col.startswith('boxCount')]][caliber_row[[col for col in caliber_row.columns if col.startswith('boxCount')]].columns[::-1]].dropna(
                    axis=1).astype(
                    float).values[0]
            from_caliber = caliber_row[[col for col in caliber_row.columns if col.startswith('caliberFrom')]].dropna(axis=1).values[0].tolist()
            to_caliber = caliber_row[[col for col in caliber_row.columns if col.startswith('caliberTo')]].dropna(axis=1).values[0].tolist()

            if caliber_row['caliberFrom1'].values[0] is None:
                from_caliber.insert(0, 0)
            if len(from_caliber) == len(to_caliber) + 1:
                to_caliber.append(inf_math)
            from_to = []
            from_to_labels = []
            for f, t in zip(reversed(from_caliber), reversed(to_caliber)):
                from_to.append((f, t))
                from_to_labels.append(str(int(f) if int(f) == float(f) else float(f)))

            # set attributes in object
            self.block_info['distribution_info']['caliber_at_picking']['interval_size'] = IntervalIndex.from_tuples(from_to, closed='right')

            self.block_info['distribution_info']['caliber_at_picking']['labels'] = array_np([str(int(count)) + '\n' + str(size) if size != 0 and size != inf_math
                                                                                             else str(int(count)) + '\n<' if size == 0 else str(int(count)) + '\n>'
                                                                                             for count, size in
                                                                                             zip(reversed(self.block_info['distribution_info']['caliber_at_picking']['box_count']),
                                                                                                 reversed(from_to_labels))], dtype=str)

            # weights
            # from origin DB
            weights_DB = \
                caliber_row[[col for col in caliber_row if col.startswith('cartonWeight')]] \
                    [caliber_row[[col for col in caliber_row if col.startswith('cartonWeight')]].columns[::-1]].astype(float).values[0]
            # set for fruit weight calculation

            weights_calc = []
            for i, w in enumerate(weights_DB):
                if i < len(from_to):
                    if isnan(w):
                        weights_calc.append(1000 * caliber_row['box_W'].squeeze())
                    else:
                        weights_calc.append(1000 * w)
                else:
                    break

            self.block_info['distribution_info']['box_W'] = weights_calc
            self.block_info['distribution_info']['caliber_at_picking']['coef_weight_unit'] = 0.45359 if caliber_row['w_unit'].squeeze().lower() == 'lb' else 1
            self.block_info['distribution_info']['caliber_at_picking']['coef_caliber_unit'] = 0.0393 if caliber_row['packing_caliber_unit'].squeeze().lower() == 'inch' else 1

            self.block_info['distribution_info']['caliber_at_picking']['weight_per_box'] = [i * self.block_info['distribution_info']['caliber_at_picking']['coef_weight_unit']
                                                                                            for i in self.block_info['distribution_info']['box_W']] / \
                                                                                           self.block_info['distribution_info']['caliber_at_picking']['box_count']
        except:
            self.set_red_flag(True)
            raise Exception('Packout metadata / Unit does not exist for current block')

    def set_historical_packout(self, season, current_packing_method):
        try:
            actual_packout = queries.get_historical_packout('"{0}"'.format(self.block_info['block_name']), season - 1)
            if len(actual_packout) == 1:
                if (actual_packout['packing_method'] == current_packing_method).values[0]:
                    actual_packout = actual_packout[[col for col in actual_packout if col.startswith('packQ')]]
                    agg_df = DataFrame(columns=[str(i + 1) for i in range(20)])
                    for i in range(5):
                        t = actual_packout[[col for col in actual_packout if col.startswith('packQ' + str(i + 1))]]
                        t.columns = [str(i + 1) for i in range(20)]
                        agg_df = concat([agg_df, t], axis=0)

                    # handle bug in portal DB with empty history packout
                    if agg_df.isnull().values.any():
                        return

                    dist = agg_df.groupby(agg_df.index).agg(['sum']).iloc[0, 0:len(self.block_info['distribution_info']['caliber_at_picking']['box_count'])].tolist()
                    self.block_info['distribution_info']['caliber_at_picking']['history_carton'] = [round((float(i) / sum(dist)) * 100, 1) for i in dist]
        except Exception as e:
            self.logger.error('Cannot get historical packout from db')
            return
    def set_size_value(self, size=None):

        if self.scan_num == 1:
            # 'size' key is the one extracted by the model tuning
            self.block_info['scans']['1st']['size'] = self.block_info['scans']['1st'][self.stat_type]
            # UI needs only
            self.block_info['scans']['1st']['medium'] = self.block_info['scans']['1st'][self.stat_type]
        elif self.scan_num == 2:
            # TODO TO BE DEFINED
            # 'size' key is the one extracted by the model tuning
            self.block_info['scans']['1st']['size'] = self.block_info['scans']['1st']['medium']
            self.block_info['scans']['2nd']['size'] = self.block_info['scans']['2nd'][self.stat_type]
            # UI needs only
            self.block_info['scans']['2nd']['medium'] = self.block_info['scans']['2nd'][self.stat_type]

    def set_stat_type(self, type):
        self.stat_type = type

    def set_top_1_model(self, model):
        self.top_1_model = model

    def get_samples(self, obj=None, coef_default=None):

        if obj is not None:
            model = obj
        elif self.top_1_model is None:
            return
        else:
            model = self.top_1_model

        coef = self.block_info['distribution_info']['caliber_at_picking']['coef_caliber_unit'] if coef_default == None else coef_default
        factor = 10
        samples = self.block_info['distribution_info']['diameter'].rolling(2).mean().rolling(2).mean().dropna()

        return {'picking_time': (samples + model.get_dynamic_variables()['delta_picking']['size']) * coef,
                'scan_time': samples * coef,
                'Future1': (samples + model.calc_delta_size(skip_days=factor * 1)) * coef,
                'Future2': (samples + model.calc_delta_size(skip_days=factor * 2)) * coef,
                'Future3': (samples + model.calc_delta_size(skip_days=factor * 3)) * coef,
                'Future4': (samples + model.calc_delta_size(skip_days=factor * 4)) * coef,
                'Future5': (samples + model.calc_delta_size(skip_days=factor * 5)) * coef,
                'Future6': (samples + model.calc_delta_size(skip_days=factor * 6)) * coef,
                'Future7': (samples + model.calc_delta_size(skip_days=factor * 7)) * coef,
                'Future8': (samples + model.calc_delta_size(skip_days=factor * 8)) * coef,
                'Future9': (samples + model.calc_delta_size(skip_days=factor * 9)) * coef}

    # get all scans points for graph view
    def get_points(self, model):
        # init scan points for view reference on model
        x, y = [], []
        abs_start_day,first_key = None, None

        # append from first scan to latest
        for scan_num in list(self.block_info['scans'].keys())[::-1]:
            if abs_start_day == None:
                abs_start_day = model.find_fixed_day(self.block_info['scans'][scan_num]['date'], delta=0)
                first_key = scan_num
            if(self.block_info['scans'][scan_num]['date']!=None):
                delta_days = (self.block_info['scans'][scan_num]['date'] - self.block_info['scans'][first_key]['date']).days
                x.append(abs_start_day + delta_days)
                y.append(self.block_info['scans'][scan_num]['mean'])
        return (x, y)

    def get_distribution(self, obj=None):
        if obj is not None:
            results_table = self.get_samples(obj)
        elif self.top_1_model is None:
            return
        else:
            results_table = self.get_samples(obj)

        # scan_time
        samples = results_table['scan_time']
        skip = settings.config['BIN_FS_INTERVAL']['skip'] * self.block_info['distribution_info']['caliber_at_picking']['coef_caliber_unit']

        min = samples.min()
        start = settings.config['BIN_FS_INTERVAL']['start'] * self.block_info['distribution_info']['caliber_at_picking']['coef_caliber_unit']
        start = int((min - start) / skip) * skip + start if min > start else start

        max = samples.max()
        end = max + skip

        size_bins = arange(start=start, stop=end, step=skip)

        # calculates distribution for 2ndscan size
        size_dist = round(cut(samples, bins=size_bins, include_lowest=True).value_counts(normalize=True).sort_index().mul(100), 1)
        size_scan_time = size_dist.reset_index().rename(columns={'index': 'bin_interval', 'diameter': 'freq'})

        # At picking_time
        predicted_samples = results_table['picking_time']
        dist = cut(predicted_samples, bins=self.block_info['distribution_info']['caliber_at_picking']['interval_size'], include_lowest=True).value_counts(normalize=True).sort_index()
        ratio = dist / self.block_info['distribution_info']['caliber_at_picking']['box_count']

        carton_picking_time = [round((float(i) / sum(ratio)) * 100, 1) for i in ratio]
        size_picking_time = around((dist * 100).to_list(), decimals=2)

        return size_scan_time, size_picking_time, carton_picking_time

    def get_dropped(self, samples):
        dropped = 0
        down = int(self.block_info['distribution_info']['caliber_at_picking']['interval_size'][-1].left)
        up = int(self.block_info['distribution_info']['caliber_at_picking']['interval_size'][0].right if self.block_info['distribution_info']['caliber_at_picking']['interval_size'][0].right!=inf_math else self.block_info['distribution_info']['caliber_at_picking']['interval_size'][0].left)

        for s in samples:
            if s > up or s < down:
                dropped += 1
        return dropped / len(samples)

    def set_red_flag(self, bool):
        self.red_flag = bool

    def get_top_1_model(self):
        return self.top_1_model

    def get_block_info(self):
        return self.block_info

    def get_scan_num(self):
        return self.scan_num

    def get_red_flag(self):
        return self.red_flag

    def get_prediction(self):
        vars = self.top_1_model.get_dynamic_variables()
        pred = vars['1st']['size'] + vars['delta_2nd']['size'] + vars['delta_picking']['size']
        return pred

    def get_stat_type(self):
        return self.stat_type

    def find_results(self):
        # TODO
        # CHECK EXISTANCE IN DB
        DB_value = None
        dir_csv = join('input', self.block_info['block_name'] + 'temp.csv')
        _resource = resource('s3', aws_access_key_id=settings.config["AWS"]["access key"], aws_secret_access_key=settings.config["AWS"]["secret key"])
        try:
            _resource.meta.client.download_file(settings.config["AWS"]["bucket"], self.block_info['scans']['1st' if self.scan_num == 1 else '2nd']['output_s3'], dir_csv)
        except ClientError:
            return False

        df = read_csv(dir_csv)
        os.remove(dir_csv)
        try:
            diff = df.iloc[5, 0] - df.iloc[5, 1]
            mean1 = df.iloc[:, 0].mean()
            mean2 = df.iloc[:, 1].mean()
            if int(mean1 - mean2) == int(diff):
                self.logger.info('Results are written in S3, size is mean')
                self.block_info['existed result'] = mean1
                return True

            mode1 = Analysis.choose_mode(df.iloc[:, 0])
            mode2 = Analysis.choose_mode(df.iloc[:, 1])
            if int(mode1 - mode2) == int(diff):
                self.logger.info('Results are written in S3, size is mode')
                self.block_info['existed result'] = mode1
                return True

            median1 = df.iloc[:, 0].median()
            median2 = df.iloc[:, 1].median()
            if int(median1 - median2) == int(diff):
                self.logger.info('Results are written in S3, size is median')
                self.block_info['existed result'] = median1
                return True

        except Exception as e:
            self.logger.error('Results are written in S3 but file is corrupted')
            return False

    def check_automation_limitation(self, var):
        if var in settings.fruits_available:
            return
        else:
            self.set_red_flag(True)
            raise Exception('automated analysis for current fruit type is not available')

    def get_written_result(self):
        return self.block_info['existed result']


class Analysis():

    def __init__(self, blockObj, logger=None):
        # settings.init()
        self.block = blockObj
        self.logger = logger if logger is not None else logging.getLogger('0')

    def run(self):
        self.samples_check()
        models = self.match_models()
        top1_model = self.select_model(models)
        self.distribution_analysis(top1_model)
        self.block.set_top_1_model(copy.deepcopy(top1_model))
        return self.block.get_prediction(), True

    def samples_check(self):
        samples = self.block.get_block_info()['distribution_info']['diameter']
        smoothed_samples = samples.rolling(2).mean().rolling(2).mean().dropna()
        if len(samples) <= 150:
            self.logger.error('Not enough samples')
            raise Exception
        else:
            shapiro_test = stats.shapiro(samples)
            mode = Analysis.choose_mode(smoothed_samples)
            mean = smoothed_samples.mean()
            median = smoothed_samples.median()

            if shapiro_test.pvalue > 0.05:
                self.logger.info('Normal distribution accepted')
                # comes from normal dist
                self.block.set_stat_type('mean')
                self.logger.info('Mean value is chosen')
            else:
                self.logger.info('Normal distribution not accepted')
                if 2 <= abs(mode - mean) <= 5:
                    self.block.set_stat_type('mode')
                    self.logger.info('Mode value is chosen')
                else:
                    if mean <= median <= mode or mode <= median <= mean:
                        self.block.set_stat_type('median')
                        self.logger.info('Median value is chosen')
                    else:
                        self.block.set_stat_type('mean')
                        self.logger.info('Mean value is chosen')

        self.block.set_size_value()

    def match_models(self):
        info = self.block.get_block_info()
        fruit_type = info['fruit_type']
        hemisphere = info["hemisphere"]
        print('hemi of block is ',hemisphere)
        picking_period = info['picking_date']
        models = []
        # normalize picking date to N hemisphere
        picking_period = picking_period if hemisphere == 'N' else picking_period + timedelta(days=182)
        varieties = settings.varieties

        for model in settings.models_objects:
            #if model.model_id=='cl_nules_sf3_mahela_rsa_2021':
           if ModelObject.fruit_type_match(model, fruit_type):
                start = ModelObject.get_date(varieties[varieties['variety_name'].str.lower() == model.get_fruit_variety()]['season_start'])
                end = ModelObject.get_date(varieties[varieties['variety_name'].str.lower() == model.get_fruit_variety()]['season_end'])
                if ModelObject.picking_period_match(start, end, picking_period):
                    #check if picking period is after more than 10 days from model end date
                    max_accumulated_day=ModelObject.get_accumulated_days_list(model).max()
                    start_m= model.start_date.date()
                    year= picking_period.year -1 if start_m.month > picking_period.month else picking_period.year
                    start_m=start_m.replace(year=year)
                    delta = 0 if model.hemisphere==hemisphere else 182
                    end_m=(start_m+timedelta(days=max_accumulated_day-delta))
                    if (picking_period-end_m).days <= 10:
                        models.append(model)
                    else:
                        print(model.model_id, ' excluded because has more than 10 days diff. Picking date is after model finish')

        if len(models) == 0:
            # raise Exception('No models were found')
            pass
        else:
            self.logger.info(str(len(models)) + ' models were found in matching')
        return models

    def select_model(self, models, manual=False):
        def select_model_2():
            model = None
            for m in models:
                m.set_dynamic_variables(info=block_info)
                score, day_opt1 = m.adjust(method='by_score')
                if day_opt1 is not None:
                    if model == None:
                        m.set_score(score)
                        model = m
                    elif model.get_score() < score:
                        m.set_score(score)
                        model = m

            if model is not None:
                self.logger.info("Model " + model.get_model_id() + " has minimum score rate : " + str(round(model.get_score(), 2)))
                _, day_opt2 = model.adjust(method='by_size')
                if day_opt2 is not None:
                    if abs(model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2)) <= 10:
                        model.set_dynamic_variables(days=day_opt2, calc_delta_size=True, diff_days=model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2))
                        self.logger.info("Model " + model.get_model_id() + " calculated by size with days difference : " + str(model.set_dynamic_variables()['1st']['diff_days']))
                    else:
                        score, day_opt1 = model.adjust(method='by_score')
                        self.logger.info("Model " + model.get_model_id() + " calculated by score days difference higher than 10")
                        model.set_dynamic_variables(days=day_opt1, calc_delta_size=True, diff_days=model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt1))
                else:
                    score, day_opt1 = model.adjust(method='by_score')
                    self.logger.info("Model " + model.get_model_id() + " calculated by score days difference higher than 10")
                    model.set_dynamic_variables(days=day_opt1, calc_delta_size=True, diff_days=model.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt1))
            else:
                self.logger.error('Failed to find a model with less than 10 days diff and proper score')
                raise Exception

            self.logger.info("Model " + model.get_model_id() + " is chosen")
            return model

        def select_model_1():
            for m in models:
                m.set_dynamic_variables(info=block_info)
                _, day_opt = m.adjust(method='by_size')
                m.set_dynamic_variables(days=day_opt, calc_delta_size=True, diff_days=m.find_fixed_day(calender_date=block_info['scans']['1st']['date'], delta=day_opt))

            models.sort(key=Analysis.sortByDiffDays)
            model = None

            for m in models:
                diff = m.get_dynamic_variables()['1st']['diff_days']
                if abs(diff) <= 10:
                    if ModelObject.fruit_variety_match(m, block_info['fruit_variety']):
                        model = m
                        break

            # if model is None:
            #     for m in models:
            #         diff = m.get_dynamic_variables()['1st']['diff_days']
            #         if diff <= 10:
            #             if ModelObject.fruit_variety_match(m, block_info['fruit_variety']):
            #                 model = m
            #                 break
            #
            # if model is None:
            #     for m in models:
            #         diff = m.get_dynamic_variables()['1st']['diff_days']
            #         if diff <= 10:
            #             if ModelObject.geographic_match(m, block_info['country']):
            #                 model = m
            #                 break

            if model is None and abs(models[0].get_dynamic_variables()['1st']['diff_days']) > 10:
                self.logger.error('Failed to find a model with less than 10 days diff')
                raise Exception
            elif model is None and not ModelObject.fruit_variety_match(models[0], block_info['fruit_variety']):
                self.logger.error('Model with less than 10 days diff has been found with no matching by variety and geo')
                raise Exception
            else:
                self.logger.info('The chosen model has ' + 'the same fruit variety' if ModelObject.fruit_variety_match(model, block_info['fruit_variety']) else 'fruit variety : ' + model.get_frui)

            self.logger.info("Model " + model.get_model_id() + " is chosen")
            return model

        def adjust_models():
            adjusted = []
            failed = 0
            for m in models:
                try:
                    m.set_dynamic_variables(info=block_info)
                    _, day_opt2 = m.adjust(method='by_size')

                    # check if by size is valid
                    if day_opt2 is not None:
                        if abs(m.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2)) <= 10:
                            m.set_dynamic_variables(days=day_opt2, calc_delta_size=True, diff_days=m.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt2))
                            m.set_score(None)
                            adjusted.append(m)
                            continue

                    # if by size is not valid and the case is 2 scans
                    # check of by score is valid
                    if self.block.get_scan_num() == 2:
                        # score methods based on 2 scans
                        _, day_opt1 = m.adjust(method='by_date',first_day=block_info['scans']['1st']['date'])
                        if day_opt1 is not None:
                            m.set_dynamic_variables(days=day_opt1, calc_delta_size=True, diff_days=m.find_fixed_day(block_info['scans']['1st']['date'], delta=day_opt1))
                            m.set_score(None)
                            adjusted.append(m)
                            continue

                    # load model anyway
                    m.set_dynamic_variables(calc_delta_size=True)
                    m.set_score(None)
                    adjusted.append(m)
                except Exception as e:
                    print(f'Select model stage: {m.get_model_id()} error: {repr(e)}')
                    failed += 1
                    pass

            return adjusted, failed

        block_info = self.block.get_block_info()
        if manual == True:
            return adjust_models()
        elif self.block.get_scan_num() == 1:
            return select_model_1()
        elif self.block.get_scan_num() == 2:
            return select_model_2()

    def distribution_analysis(self, model):
        info = self.block.get_block_info()['distribution_info']['caliber_at_picking']
        dropped_ratio = self.block.get_dropped(self.block.get_samples(obj=model)['picking_time'])
        if dropped_ratio > 0.2:
            raise Exception('More than 20% samples were dropped')

        if info['history_carton'] is not None:
            if not Analysis.compare_distributions(info['history_carton'], info['current_carton']):
                raise Exception('History packout points on more than 1 bin count in peak difference')

    @staticmethod
    def compare_distributions(list1, list2):
        index1 = argmin(list1)
        index2 = argmin(list2)

        if abs(index1 - index2) >= 1:
            return False
        else:
            return True

    @staticmethod
    def sortByDiffDays(arg):
        return arg.get_dynamic_variables()['1st']['diff_days']

    @staticmethod
    def choose_mode(samples):
        diff = math.inf
        mode = None
        for i, var in samples.round().mode().items():
            if abs(var - samples.mean()) < diff:
                diff = abs(var - samples.mean())
                mode = var
        return mode


class Result():
    def __init__(self, block, model=None):
        # settings.init(False)
        self.stat_type = block.get_stat_type()
        self.id = Result.set_id(block, model)
        self.s3_pathS = Result.select_s3_paths(scans = block.get_block_info()["scans"],scan_number=block.get_scan_num())
        self.local_path = block.get_block_info()['path_local']['output']

        self.caliber_info = block.get_block_info()['distribution_info']['caliber_at_picking']
        size_scan_time, size_picking_time, carton_picking_time = block.get_distribution(model)

        packout = {'weight_per_count': self.caliber_info['weight_per_box'],
                   'customer count': self.caliber_info['box_count'],
                   'mm range': self.caliber_info['interval_size'],
                   'carton distribution-p': carton_picking_time,
                   'size distribution-p': size_picking_time,
                   'avg weight': None,
                   'final weight': None,
                   '': None}
        df_2ndscan = size_scan_time.rename(columns={'bin_interval': '2nd scan FSbin', 'freq': 'size distribution-c'})
        self.df_dist = concat([DataFrame.from_dict(packout), df_2ndscan], axis=1)

        # calculated according to mm unit
        self.df_samples = concat([DataFrame.from_dict(block.get_samples(model, 1)),
                                  DataFrame.from_dict({'ModelID': [self.id]})], axis=1)

        # return the relevant varieties to calc weight according
        self.weights_DB = Result.get_weights(info=block.get_block_info(), df=block.block_info['fruit_variety'])

    @staticmethod
    def set_id(block, model):
        if model is None:
            return block.get_top_1_model().get_model_id()
        else:
            return model.get_model_id()

    @staticmethod
    def get_weights(info, df, list=None):
        df = settings.size_to_weight
        if list is None:
            pd = info["picking_date"]
            hemisphere = info["hemisphere"]
            pd = pd if hemisphere == "N" else pd + timedelta(days=182)
            varieties = settings.varieties
            list_var = [var for var in df[df['fruit_type'] == info["fruit_type"]].fruit_variety.unique()
                        if ModelObject.picking_period_match(start=ModelObject.get_date(varieties[varieties['variety_name'].str.lower() == var.replace('_', ' ')]['season_start']),
                                                            end=ModelObject.get_date(varieties[varieties['variety_name'].str.lower() == var.replace('_', ' ')]['season_end']),
                                                            pd=pd)]
        else:
            list_var = list
        df_var = DataFrame()
        for var in list_var:
            df_var = concat([df_var, df[var == df['fruit_variety'].str.replace('_', ' ')]], axis=0)
        return df_var

    @staticmethod
    def select_s3_paths(scans,scan_number):
        pathS = []
        YS = False
        caliper = False

        for scan_key in scans.keys():
            if scans[scan_key]['bucket'] == settings.config["AWS"]['caliper_bucket'] and not caliper:
                caliper = True
                pathS.append((scans[scan_key]["bucket"],scans[scan_key]["output_s3"]))
            elif scans[scan_key]['bucket'] == settings.config["AWS"]['YS_bucket'] and not YS:
                YS = True
                if scan_number == 2:
                    pathS.append((scans['2nd']["bucket"],scans['2nd']["output_s3"]))
                elif scan_number == 1:
                        pathS.append((scans['1st']["bucket"],scans['1st']["output_s3"]))

            if YS and caliper:
                break

        return pathS

    def set_weights(self):
        # calculations for weight that extracted from boxes count and ratio
        self.df_dist.at[0, 'avg weight'] = Result.weight_from_carton(samples=self.df_samples['picking_time'].loc[1:], caliber_info=self.caliber_info)
        # weight from table
        self.df_dist.at[1, 'avg weight'] = Result.weight_from_DB(self.weights_DB, samples=self.df_samples['picking_time'].loc[1:], stat_type=self.stat_type)
        # avg both calculations weight
        self.df_dist.at[2, 'avg weight'] = self.df_dist['avg weight'].loc[0:1].mean()

        # adjusted weight values to each period
        for col in self.df_samples.columns:
            if col == 'scan_time' or col == 'ModelID':
                continue
            w1 = Result.weight_from_carton(samples=self.df_samples[col].loc[1:], caliber_info=self.caliber_info)
            w2 = Result.weight_from_DB(self.weights_DB, samples=self.df_samples[col].loc[1:], stat_type=self.stat_type)
            w = Result.pick_weight(w1, w2)
            self.df_samples.at[0, col] = w

    def get_left_graph(self):
        return self.df_dist['2nd scan FSbin'].dropna(), self.df_dist['size distribution-c'].dropna()

    def get_right_graph(self):
        return self.df_dist['carton distribution-p'].dropna(), self.caliber_info['history_carton'], self.caliber_info['labels']

    def get_model_id(self):
        return self.id

    def save_dist(self):

        block_path_csv = path.join(self.local_path, self.id + '.csv')
        self.df_dist.to_csv(block_path_csv, index=False)

        block_path_png = path.join(self.local_path, self.id + '.png')
        sketch = sizeDistribution(self)
        sketch.fig.savefig(block_path_png)

    def save_samples(self, path_local=False, path_s3=False):

        local_save = path.join(self.local_path, self.id + '_samples.csv')
        print('local save : ', local_save)
        self.df_samples.to_csv(local_save, index=False)

        if path_s3:
            for bucket, output_s3_path in self.s3_pathS:
                _resource = resource('s3', aws_access_key_id=settings.config["AWS"]["access key"], aws_secret_access_key=settings.config["AWS"]["secret key"])
                #TODO remove remark
                _resource.meta.client.upload_file(local_save, bucket, output_s3_path)
        # if not path_local:
        #     remove(local_save)

    @staticmethod
    def weight_from_DB(df, samples, stat_type):
        def stat_size():
            if stat_type == "Mode":
                size = Analysis.choose_mode(samples)
                return round(size - 0.5), round(size + 0.5)
            else:
                return round(samples.mean() - 0.5), round(samples.mean() + 0.5)

        if df.empty:
            return None
        else:
            round_down, round_up = stat_size()
            const1 = round_down < df['width_per_sample']
            const2 = df['width_per_sample'] < round_up
            return df[const1 & const2]['mean_weight_per_fruit'].mean()

    @staticmethod
    def weight_from_carton(samples, caliber_info):
        dist = cut(samples * caliber_info['coef_caliber_unit'], bins=caliber_info['interval_size'], include_lowest=True).value_counts(normalize=True).sort_index()
        ratio = dist / caliber_info['box_count']
        dist = [round((float(i) / sum(ratio)) * 100, 1) for i in ratio]
        mul = [i / 100 for i in dist] * caliber_info['box_count']
        size_pred_dist = mul / mul.sum()
        weight = nansum(caliber_info['weight_per_box'] * size_pred_dist)
        return weight

    @staticmethod
    def pick_weight(w1, w2):
        if isna(w2):
            return w1
        if abs(w1-w2)/w1 >= 0.2:
            return w1
        return mean([w1, w2])
