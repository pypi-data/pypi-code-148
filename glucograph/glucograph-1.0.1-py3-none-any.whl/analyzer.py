#!/usr/bin/env python
# This file loads data from two sources: xDrip sqlite database and
# glucometer readings. Then it tries to analyze which nights were
# good (without low BS), and which ones are bad. Then it compares
# BS levels for the previous day to find correlation.

import enum
import csv
import numpy as np
import logging
from dataclasses import dataclass
import sqlite3
import datetime as dt
from typing import List, Tuple, Any


class BgSources(enum.Enum):
    BG_READINGS = 1,
    BLOOD_TEST = 2,
    TREATMENTS = 3,
    GLUCOMETER = 4


class Treatments(enum.Enum):
    NONE = 0,
    GLUCO_TAB = 1,
    SNACK = 2


class GlucoseUnits(enum.Enum):
    MMOL_L = 'mmol/l'
    MG_DL = 'mg/dl'


# This mapping translates human strings entered on phone to normalized values.
# Currently, it is not used in charts or statistics.
TREATMENTS_MAP = {
    "tableta": Treatments.GLUCO_TAB,
    'palcka': Treatments.SNACK,
    "1 tableta": Treatments.GLUCO_TAB,
    '1 palcka': Treatments.SNACK,
    'Sensor session was restarted': Treatments.NONE,
    'Started by transmitter': Treatments.NONE,
    'Stopped by transmitter: Stopped': Treatments.NONE,
    'Stopped by transmitter: Sensor Failed Start': Treatments.NONE,
    'Started by xDrip': Treatments.NONE,
    'Stopped by xDrip': Treatments.NONE
}


class BgSample:
    def __init__(self, source: BgSources, timestamp: dt.datetime, bg_value_mmol_l: float):
        self.source = source
        self.timestamp = timestamp
        self.bg_value_mmol_l = bg_value_mmol_l
        self.treatment = None
        self.desc = ''  # description of treatment

    def set_treatment(self, treatment: Treatments):
        self.treatment = treatment

    def set_desc(self, desc: str):
        self.desc = desc

    def __str__(self):
        return f'src: {self.source}, ' \
               f'time: {self.timestamp}, ' \
               f'bg: {self.bg_value_mmol_l:.1f}, ' \
               f'treat: {self.treatment}' \
               f'desc: {self.desc}'

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other: "BgSample"):
        return self.timestamp < other.timestamp


@dataclass
class MealData:
    meal_time: dt.time
    line_style: str  # contains matplotlib color and style, for example 'r:'
    description: str  # short meal description shown in the top chart


def mg_per_dl_to_mmol_per_l(mg_per_dl: float) -> float:
    return mg_per_dl / 18


def mmol_per_l_to_mg_per_dl(mmol_per_l: float) -> float:
    return mmol_per_l * 18


def to_selected_unit(value_mmol_l: float, unit: GlucoseUnits):
    """
    Converts value in mmol/l to selected unit.
    """
    return value_mmol_l if unit == GlucoseUnits.MMOL_L else mmol_per_l_to_mg_per_dl(value_mmol_l)


def list_to_selected_unit(values_mmol_l: List[float], unit: GlucoseUnits):
    """
    Converts values in list in mmol/l to selected unit.
    """
    if unit == GlucoseUnits.MG_DL:
        for i in range(len(values_mmol_l)):
            values_mmol_l[i] = mmol_per_l_to_mg_per_dl(values_mmol_l[i])


def read_table_bg_readings(db: sqlite3.Connection) -> List[BgSample]:
    """
    This table contains blood glucose values from xDrip source (e.g. Dexcom G6).
    """
    bg_samples: List[BgSample] = []
    for row in db.execute("select timestamp, calculated_value from BgReadings"):
        logging.debug(row)
        bg_samples.append(BgSample(BgSources.BG_READINGS,
                                   dt.datetime.fromtimestamp(row[0]/1000),
                                   mg_per_dl_to_mmol_per_l(float(row[1]))))
    bg_samples.sort()
    return bg_samples


def read_table_blood_test(db: sqlite3.Connection) -> List[BgSample]:
    """
    This table contains data from finger pricking (glucometer) stored by xDrip.
    This is subset of all reading from glucometer, because we
    do not enter BG value to xDrip, when difference is less than 0.5 mmol/l.
    """
    bg_samples: List[BgSample] = []
    for row in db.execute("select created_timestamp, mgdl, source from BloodTest"):
        logging.debug(row)
        # source = row[2]  # ignored, can be either: 'Manual Entry' or 'Initial Calibration'
        bg_samples.append(BgSample(BgSources.BLOOD_TEST,
                                   dt.datetime.fromtimestamp(row[0]/1000),
                                   mg_per_dl_to_mmol_per_l(float(row[1]))))
    bg_samples.sort()
    return bg_samples


def read_table_treatments(db: sqlite3.Connection) -> List[BgSample]:
    """
    This table contains manually entered events, for example food eaten on low
    BG events.
    """
    bg_samples: List[BgSample] = []
    for row in db.execute("select notes, timestamp from Treatments"):
        logging.debug(row)
        bg_sample = BgSample(BgSources.TREATMENTS,
                             dt.datetime.fromtimestamp(row[1]/1000),
                             0)
        if row[0] is not None:  # if nothing was entered, there is no useful data
            if row[0] in TREATMENTS_MAP:
                treatment = TREATMENTS_MAP[row[0]]
            else:
                treatment = Treatments.NONE

            bg_sample.set_treatment(treatment)
            bg_sample.set_desc(row[0])
            bg_samples.append(bg_sample)

    bg_samples.sort()
    return bg_samples


def read_glucometer_data(fname: str) -> List[BgSample]:
    """
    This function reads data in CSV format retrieved via USB from glucometer.
    Glucometer data can provide information about accuracy of G6. If there is
    glucometer value measured close to G6 value, and higher, it means there was
    no low BS event.
    """
    bg_samples = []
    with open(fname, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, skipinitialspace=True)
        for row in csv_reader:
            date_time = dt.datetime.fromisoformat(row[0])
            bg_samples.append(BgSample(BgSources.GLUCOMETER, date_time, float(row[1])))

    return bg_samples


def read_glucometer_files(fnames: List[str]) -> List[BgSample]:
    gmeter_samples: List[BgSample] = []
    for gmeter_fname in fnames:
        logging.debug(f"Reading glucometer csv file: {gmeter_fname}")
        bg_samples = read_glucometer_data(gmeter_fname)
        gmeter_samples.extend(bg_samples)

    return gmeter_samples


def read_meals(fname: str) -> List[MealData]:
    meal_data = []
    with open(fname) as meals_file:
        csv_reader = csv.reader(meals_file, skipinitialspace=True)
        for row in csv_reader:
            time = dt.datetime.strptime(row[0], '%H:%M').time()
            meal = MealData(time, line_style=row[1], description=row[2])
            meal_data.append(meal)

    return meal_data


def extract(x: List[Any], y: List[float], filter_func) -> List[Tuple[List[Any], List[float]]]:
    """
    Extracts all items from `y`, which pass `filter_func`, and groups consecutive 
    items into segments. Elements from `x`, which are at the same index at 
    matching items from `y`, are put into the first list.
    Example of usage: If we have list of x and list of y value for a chart, and
    we want to get segments of line above or below some value.
    """
    extracted_segments: List[Tuple[List[Any], List[float]]] = []
    segment_x = []
    segment_y = []
    prev_idx = len(x)
    for idx, val in enumerate(y):
        if filter_func(val):
            if idx - prev_idx > 1:  # if there was an item between samples, start new segment
                extracted_segments.append((segment_x, segment_y))
                segment_x = []
                segment_y = []
            segment_x.append(x[idx])
            segment_y.append(val)
            prev_idx = idx

    if segment_x:
        extracted_segments.append((segment_x, segment_y))

    return extracted_segments


BG_STEP = 0.5
MAX_BG_VALUE = 10  # in mmol/l, should never be measured


def analyze_meter_cgm_diff(gmeter_samples: List[BgSample],
                           cgm_samples: List[BgSample]) -> Tuple[List[float], List[float]]:
    """
    This function analyzes differences between glucometer and CGM. Not very
    useful at the moment, since mean value is close to 0 even if there are large
    positive and negative errors. Fix it to use absolute diff.
    """
    meter_values: List[float] = []
    diffs: List[float] = []

    for gmeter_sample in gmeter_samples:
        meter_date_time = gmeter_sample.timestamp
        meter_value = gmeter_sample.bg_value_mmol_l

        low_idx = 0
        high_idx = len(cgm_samples) - 1

        while True:
            middle_idx = (high_idx + low_idx) // 2

            # we want to get cgm value just BEFORE it is corrected by entering
            # meter value
            if cgm_samples[middle_idx].timestamp == meter_date_time:
                # is it this value or one before
                print('cgm time  ==  meter time, check manually which value applies???')
                # middle_idx -= 1 # to be sure take previous value
                break
            elif cgm_samples[middle_idx].timestamp < meter_date_time:
                low_idx = middle_idx
            else:
                high_idx = middle_idx

            # print(low_idx, high_idx, middle_idx, 'cgm time : meter time  ',
            #       cgm_samples[middle_idx].timestamp, meter_date_time)
            if high_idx - low_idx <= 1:
                break

        cgm_date_time = cgm_samples[low_idx].timestamp
        cgm_value = cgm_samples[low_idx].bg_value_mmol_l

        # up to 5 minutes diff is OK, because CGM samples at 5 min interval
        # greater diff may occur when sensor is started and calibrated after 2 hours -
        # there is no sensor value for 2 hours in this case - once per week.
        if (meter_date_time - cgm_date_time).seconds <= 300:
            value_diff = meter_value - cgm_value
            meter_values.append(meter_value)
            diffs.append(value_diff)
            # print('cgm    ', middle_idx, cgm_date_time, cgm_value)
            # print('meter  ', middle_idx, meter_date_time, meter_value, '\n')

    print('no of diffs: ', len(diffs))
    print('min diff: ', min(diffs))
    print('max diff: ', max(diffs))
    print('average diff, std. dev: ', np.mean(diffs), np.std(diffs))

    diffs_of_bg = []   # this array will contain subarrays of differences.
                       # Each subaray will contain differences between meter
                       # and cgm value, for meter values, which are inside BG
                       # range covered by array.
                       # BG range = [subarrayIndex * BG_STEP, subarrayIndex * BG_STEP + BG_STEP]
    for idx in range(int(MAX_BG_VALUE/BG_STEP)):
        diffs_of_bg.append([])

    for idx in range(len(diffs)):
        d_idx = int(meter_values[idx] / BG_STEP)
        diffs_of_bg[d_idx].append(diffs[idx])

    # print(diffs_of_bg)
    average_diff_as_function_of_meter_value = []
    for diffList in diffs_of_bg:
        if diffList:
            average_diff_as_function_of_meter_value.append(np.mean(diffList))
        else:
            average_diff_as_function_of_meter_value.append(0)

    return diffs, average_diff_as_function_of_meter_value


def print_stats(bg_samples: List[BgSample]):
    """
    Prints some statistics to stdout.
    """
    print('date/time interval: ', bg_samples[0].timestamp, '-', bg_samples[-1].timestamp)
    print('no of days: ', bg_samples[-1].timestamp.date() - bg_samples[0].timestamp.date())

    print('no of measurements: ', len(bg_samples))
    bg_values = [bg_sample.bg_value_mmol_l for bg_sample in bg_samples]
    print('mean = ', np.mean(bg_values), '   std dev  = ', np.std(bg_values))
