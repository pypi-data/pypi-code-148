# This is a model object for Dana.
import math
from numpy import max as maxnp, array
from datetime import timedelta, date
import datetime
from pickle import load as load_pkl

# Constructor
import settings


class ModelObject:
    def __init__(self, row, samples):
        # settings.init(models=False)
        self.model_id = row['model_id'].lower()
        self.fruit_type = row['fruit_type'].lower()
        self.fruit_variety = row['fruit_variety'].lower()
        self.soil_type = row['soil_type'].lower()
        self.planting_year = str(row['planting_year']).replace(".0", "")
        self.rootstock = row['rootstock'].lower()
        self.crop_load = row['crop_load'].lower()
        self.DAFB = 'pending'
        self.start_date = datetime.datetime.strptime(row['start_date'], '%d/%m/%Y').replace(year=date.today().year)
        self.area = row['area'].lower()

        self.model_formula = self.set_model_formula(row["model_formula"])
        self.size_list = self.get_col(samples, 'size')
        self.accumulated_days_list = self.get_col(samples, 'accumulated_days')
        self.dates_list = self.dates_list_function()

        self.hemisphere = settings.countries[[any([kw in r for kw in self.area.split("_")]) for r in settings.countries["country"]]]['hemisphere'].values[0]
        self.same_hemi = None

        '''Later set'''
        self.dynamic_variables = {'1st': {'day': None, 'size': None, 'diff_days': None},
                                  'delta_2nd': {'day': None, 'size': None},
                                  'delta_picking': {'day': None, 'size': None}}

        self.min_score = ''
    def get_optimized_model(self, use_case):
        measured_1st_size = self.dynamic_variables['1st']['size']
        abs_1st_day = self.dynamic_variables['1st']['day']
        measured_2nd_size = measured_1st_size + self.dynamic_variables['delta_2nd']['size']
        abs_2nd_day = abs_1st_day + self.dynamic_variables['delta_2nd']['day']
        picking_size = measured_2nd_size + self.dynamic_variables['delta_picking']['size']
        picking_day = abs_2nd_day + self.dynamic_variables['delta_picking']['day']

        if use_case == 'graph':
            return [[abs_1st_day, abs_2nd_day, picking_day],
                    [measured_1st_size, measured_2nd_size, picking_size]]
        if use_case == 'boxes':
            return picking_size, abs_1st_day

    # a function receiving a dataframe and the column to tern into a list, and returning the list from the received column of the specific model_id in the DataFrame
    def get_col(self, samples, column):
        list_of_size = samples[column].tolist()
        return list_of_size

    # a function converting the start date and the accumulated days list into dates list
    def dates_list_function(self):
        dates_list = list()
        for day in self.accumulated_days_list:
            dates_list.append(self.start_date + timedelta(days=day))
        return dates_list

    # getter method for min score
    def get_score(self):
        return self.min_score

    # setter method for min score
    def set_score(self, score):
        self.min_score = round(score, 2) if score != None else score

    def get_labels_to_graph(self):
        # 1st scan
        fst_date = '{0} diff\n{1}'.format(self.dynamic_variables['1st']['diff_days'], self.get_calendar_point(self.dynamic_variables['1st']['day']))
        # 2nd scan
        if self.dynamic_variables['delta_2nd']['size'] is not 0:
            sc_date = '{0}'.format((self.get_calendar_point(self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'])))
        else:
            sc_date = ''
        # picking
        pick_date = self.get_calendar_point(self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'] + self.dynamic_variables['delta_picking']['day'])
        pick_value_cal = str(round(self.dynamic_variables['1st']['size'] + self.dynamic_variables['delta_2nd']['size'] + self.dynamic_variables['delta_picking']['size'], 2))
        pick_label = ' {0}\n{1}\nscore: {2}'.format(pick_value_cal, pick_date, str(self.min_score))
        pick_value_model = float(self.model_formula.__call__(self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'] + self.dynamic_variables['delta_picking']['day']))

        labels = {'1st': fst_date, '2nd': sc_date, 'pick': pick_label, 'model_value': pick_value_model}
        return labels

    # getter method for dynamic_variables
    def get_dynamic_variables(self):
        return self.dynamic_variables

    # setter method for dynamic_variables
    def set_dynamic_variables(self, calc_delta_size=False, days=None, info=None, diff_days=None, manual_picking_size=None):
        if info is not None:
            # block country
            self.set_hemisphere(block_hemisphere=info['hemisphere'])
            self.dynamic_variables['1st']['day'] = self.find_fixed_day(info['scans']['1st']['date'])
            self.dynamic_variables['1st']['size'] = info['scans']['1st']['size']
            self.dynamic_variables['1st']['diff_days'] = 0

            if info['scans']['2nd']['date'] is not None:
                self.dynamic_variables['delta_2nd']['day'] = (info['scans']['2nd']['date'] - info['scans']['1st']['date']).days
                self.dynamic_variables['delta_2nd']['size'] = info['scans']['2nd']['size'] - info['scans']['1st']['size']
                temp_picking_delta_days = (info['picking_date'] - info['scans']['2nd']['date']).days

            elif info['scans']['2nd']['date'] is None:
                self.dynamic_variables['delta_2nd']['day'] = 0
                self.dynamic_variables['delta_2nd']['size'] = 0
                temp_picking_delta_days = (info['picking_date'] - info['scans']['1st']['date']).days

            # check days limit for model
            max_accumolated_day = int(maxnp(self.model_formula.x.__array__()))
            self.dynamic_variables['delta_picking']['day'] = temp_picking_delta_days \
                if temp_picking_delta_days + self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'] <= max_accumolated_day \
                else max_accumolated_day - (self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'])

        if diff_days is not None:
            self.dynamic_variables['1st']['diff_days'] = diff_days

        if days is not None:
            if diff_days is None:
                self.dynamic_variables['1st']['diff_days'] = (days - self.dynamic_variables['1st']['day']) + self.dynamic_variables['1st']['diff_days']
            self.dynamic_variables['1st']['day'] = days

        if calc_delta_size is True:
            self.dynamic_variables['delta_picking']['size'] = self.calc_delta_size()

        if manual_picking_size is not None:
            self.dynamic_variables['delta_picking']['size'] = manual_picking_size - (self.dynamic_variables['1st']['size'] +
                                                                                     self.dynamic_variables['delta_2nd']['size'] +
                                                                                     self.dynamic_variables['delta_picking']['size']) + self.dynamic_variables['delta_picking']['size']

    # getter method for size_list
    def get_size_list(self):
        return array(self.size_list)

    # getter method for accumulated_days_list
    def get_accumulated_days_list(self):
        return array(self.accumulated_days_list)

    # getter method for dates_list
    def get_dates_list(self):
        return self.dates_list

    # setter model formula object from ".pkl" dependency
    def set_model_formula(self, model_formula_id):
        with open('dep\\interpolator.pkl', 'rb') as file:
            formulas = load_pkl(file)
        try:
            return formulas[model_formula_id]
        except Exception:
            return None

    def get_model_id(self):
        # str
        return self.model_id

    def get_fruit_type(self):
        # str
        return self.fruit_type

    def get_fruit_variety(self):
        # str
        return self.fruit_variety

    def get_soil_type(self):
        # str
        return self.soil_type

    def get_rootstock(self):
        # str
        return self.rootstock

    def get_planting_year(self):
        # str
        return self.planting_year

    def get_area(self):
        # str
        return self.area

    def get_crop_load(self):
        # str
        return self.crop_load

    def get_DAFB(self):
        # str
        return self.DAFB

    def get_model_formula(self):
        # PPoly
        return self.model_formula

    def get_goldenStatus(self):
        return self.goldenModel

    def set_hemisphere(self, block_hemisphere):
        self.same_hemi = self.hemisphere == block_hemisphere

    # calc calender point by accumulated day is given
    def get_calendar_point(self, int_day, string=True):
        date = self.start_date + timedelta(days=int_day)
        # in case of using for calc
        if string == False:
            return date.date()
        # in case of using for UI display
        elif string == True:
            display_date = date.strftime("%d/%m")
            return display_date

    # def simulate_pred_from1stscan(self):
    #     fstscan_size = self.graph_info[1][0]
    #     scscan_size = self.graph_info[1][1]
    #     fstscan_day = self.graph_info[0][0]
    #     scscan_day = self.graph_info[0][1]
    #
    #     norm_factor = fstscan_size / self.model_formula.__call__(fstscan_day)
    #
    #     max_accumolated_day = int(maxnp(self.model_formula.x.__array__()))
    #
    #     # check if scscan_day is in formula range
    #     if scscan_day <= max_accumolated_day:
    #         delta_size = (self.model_formula.__call__(scscan_day) - self.model_formula.__call__(fstscan_day)) * norm_factor
    #         pred_size = fstscan_size + delta_size
    #         accu = 100 - int((abs(pred_size - scscan_size) / scscan_size) * 100)
    #         self.simu_2ndscan_accu = '{0}%'.format(str(accu))

    # new logic
    def calc_delta_size(self, skip_days=0):
        day_opt = self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day']
        temp_picking_day= self.dynamic_variables['1st']['day'] + self.dynamic_variables['delta_2nd']['day'] + self.dynamic_variables['delta_picking']['day'] + skip_days
        picking_day = temp_picking_day if temp_picking_day<= int(maxnp(self.model_formula.x.__array__())) else int(maxnp(self.model_formula.x.__array__()))
        norm_factor = (self.dynamic_variables['1st']['size'] + self.dynamic_variables['delta_2nd']['size']) / \
                      self.model_formula.__call__(day_opt)

        # check if picking_day is in formula range
        delta_size = (self.model_formula.__call__(picking_day) - self.model_formula.__call__(day_opt)) * norm_factor

        return delta_size

    def adjust(self, method,first_day=None):
        minimize = math.inf
        day_opt = None

        max_accumolated_day = int(maxnp(self.model_formula.x.__array__()))

        if method == 'by_date':
            day_opt=(first_day-self.start_date.date()).days
            if self.same_hemi:
                day_opt= day_opt if day_opt>0 else day_opt+365
            else:
                day_opt = day_opt if day_opt > 0 else day_opt + 182

        else:
            for day in range(0, max_accumolated_day - self.dynamic_variables['delta_2nd']['day']):
                y1 = self.model_formula.__call__(day)

                if method == 'by_score':
                    # shouldn't be 0
                    slope_scan = abs(self.dynamic_variables['delta_2nd']['size']) / abs(self.dynamic_variables['delta_2nd']['day'])
                    y2 = self.model_formula.__call__(day + self.dynamic_variables['delta_2nd']['day'])
                    delta_y = y2 - y1
                    slope_model = abs(delta_y) / abs(self.dynamic_variables['delta_2nd']['day'])

                    diff_slope = abs(slope_model - slope_scan)
                    diff_days = abs(day - self.dynamic_variables['1st']['day'])



                    optional_score = self.score(diff_days, diff_slope)

                    if optional_score < minimize:
                        minimize = optional_score
                        day_opt = day



                elif method == 'by_size':
                    if abs(y1 - self.dynamic_variables['1st']['size']) < minimize:
                        minimize = abs(y1 - self.dynamic_variables['1st']['size'])
                        day_opt = day

        return minimize, day_opt

    def score(self, diff_days, diff_slope):
        days = diff_days / settings.config["function"]["Norm_values"]["days"]
        slope = diff_slope / settings.config["function"]["Norm_values"]["slope"]
        if diff_days <= 10:
            return days * settings.config["function"]["alpha"]["1"] + slope * (1 - settings.config["function"]["alpha"]["1"])
        elif diff_days <= 25:
            return days * settings.config["function"]["alpha"]["2"] + slope * (1 - settings.config["function"]["alpha"]["2"])
        else:
            return days * settings.config["function"]["alpha"]["3"] + slope * (1 - settings.config["function"]["alpha"]["3"])

    def find_fixed_day(self, calender_date, delta=0):
        try:
            #calender_date = calender_date.replace(year=date.today().year)
            if self.same_hemi:
                model_year=calender_date.year
                model_date=(self.start_date.date()).replace(year=model_year)
                tmp_diff=(calender_date-model_date).days
                if tmp_diff<0:
                    model_year=model_year-1
                    start_date=model_date.replace(year=model_year)
                    model_date = (start_date + timedelta(days=delta))
                    diff=abs((calender_date - model_date).days)

                else:
                    start_date=(self.start_date.date()).replace(year=model_year)
                    model_date = (start_date + timedelta(days=delta))
                    diff = abs((calender_date - model_date).days)

            else :
                model_year=calender_date.year
                model_date = (self.start_date.date()+ timedelta(days=182)).replace(year=model_year)
                tmp_diff=(calender_date-model_date).days
                if tmp_diff<0:
                    model_year = model_year - 1
                    start_date = model_date.replace(year=model_year)
                    model_date = (start_date + timedelta(days=delta))
                    diff = abs((calender_date - model_date).days)
                else:
                    start_date = (self.start_date.date()+ timedelta(days=182)).replace(year=model_year)
                    model_date = (start_date + timedelta(days=delta))
                    diff=abs((calender_date - model_date).days)

        except ValueError:
            # in case of 29/2
            return self.find_fixed_day(calender_date + timedelta(days=1), delta)
        return diff


    @staticmethod
    def fruit_type_match(model, type):
        if model.get_fruit_type() == type.lower():
            return True
        return False

    @staticmethod
    def fruit_variety_match(model, var):
        # assuming that fruit_variety in model_info.csv is a subset of agronomy_name from portal
        splitted_var = model.get_fruit_variety().lower().split(' ') + [model.get_fruit_variety().lower()]
        for seq in splitted_var:
            if var.lower().__contains__(seq):
                return True
        return False

    @staticmethod
    def picking_period_match(start,end, pd):
        try:
            #(_start, _end) = (pd.year, pd.year+1) if start.month > end.month else (pd.year, pd.year)
            (_start, _end) = (pd.year-1, pd.year) if start.month > end.month else (pd.year, pd.year)
            if start.replace(year=_start) <= pd <= end.replace(year=_end):
                return True
        except:
            pass
        return False

    @staticmethod
    def get_date(s):
        try:
            day = str(settings.config['periodTime'][s.values[0].split(' ')[0].capitalize()])
            month = s.values[0].split(' ')[1].capitalize()
            s = "{0} {1}".format(str(day), month)
            return datetime.datetime.strptime(s, '%d %B').date()
        except:
            return None

    @staticmethod
    def geographic_match(model, var):
        # TODO
        if settings.geo_dict(model.get_area().split("_")[-1]) == settings.geo_dict(var):
            return True
        return False


class goldenModelObject(ModelObject):

    def __init__(self, *args):
        self.__dict__ = args[0].__dict__.copy()
