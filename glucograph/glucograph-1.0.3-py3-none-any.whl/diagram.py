#!/usr/bin/python3

# (c) Marko Klopčič, 2015-2023

import datetime as dt
import logging

import numpy as np
import pylab as pyl
import bisect
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from typing import List, Tuple

from glucograph.analyzer import BgSample, BgSources, MealData, GlucoseUnits
from glucograph.analyzer import list_to_selected_unit, extract


# tags in XML file
TAG_METER_READINGS = 'MeterReadings'
TAG_GLUCOSE_READINGS = 'GlucoseReadings'
TAG_EVENT_MARKERS = 'EventMarkers'

TAG_METER = 'Meter'
TAG_GLUCOSE = 'Glucose'

ATTR_DISPLAY_TIME = 'DisplayTime'
ATTR_VALUE = 'Value'

FOOD_COLOR = 'm'        # magenta
CORNSTARCH_COLOR = 'c'  # cyan

BG_STEP = 0.5


def plot_stats():
    """
    This function is not finished!
    """

    cgmMeterDiffs, averageDiffAsFunctionOfMeterValue = \
                analyzeMeterCgmDiff(meterDTValuesTuples, cgmDTValuesTuples)

    pyl.subplot(221)
    pyl.hist(listOfAllMeterValues, bins=40)
    pyl.ylabel('meter')
    pyl.xlabel('mmol/l')

    pyl.subplot(222)
    pyl.hist(listOfAllCgmValues, bins=40)
    pyl.ylabel('cgm-dex')
    pyl.xlabel('mmol/l')

    pyl.subplot(223)
    pyl.hist(cgmMeterDiffs, bins=20)
    pyl.ylabel('no of diffs')
    pyl.xlabel('mmol/l')

    pyl.subplot(224)
    # list(range(0, len(averageDiffAsFunctionOfMeterValue))
    pyl.plot(np.arange(0, len(averageDiffAsFunctionOfMeterValue) * BG_STEP, BG_STEP),
             averageDiffAsFunctionOfMeterValue)
    pyl.title('Average diff at given meter BG range (meter - cgm)')
    pyl.ylabel('average diff value')
    pyl.xlabel('mmol/l')

    pyl.show()
    return


def plot_cgm_data(cgm_samples: List[BgSample],
                  gmeter_samples: List[BgSample],
                  treatments_samples: List[BgSample],
                  gluco_unit: GlucoseUnits,
                  meals: List[MealData],
                  start_date: dt.datetime, 
                  no_of_days: int,
                  y_min: float, y_max: float, 
                  is_save_only: bool, 
                  ref_min: float,
                  ref_max: float):
    """
    This function plots CGM measurements, test measurements, treatments and
    finger prick measurements.
    """
    y_range = y_max - y_min
    font_prop = font_manager.FontProperties(size=8)

    one_day = dt.timedelta(days=1)
    day_idx = 0
    start_sample = BgSample(BgSources.BG_READINGS, start_date, 0)

    f, axes = plt.subplots(no_of_days, sharex=True, sharey=True)

    cgm_start_idx = bisect.bisect_left(cgm_samples, start_sample)
    bg_test_start_idx = bisect.bisect_left(gmeter_samples, start_sample)
    treat_start_idx = bisect.bisect_left(treatments_samples, start_sample)
    end_sample_time = start_date + one_day

    while day_idx < no_of_days:
        axes[day_idx].xaxis.set_major_formatter(mpl.dates.DateFormatter("%H:%M"))
        axes[day_idx].set_ylim(y_min, y_max)
        axes[day_idx].set_xlim(dt.datetime(start_date.year, start_date.month, start_date.day,
                                           0, 0, 0),
                               dt.datetime(start_date.year, start_date.month, start_date.day,
                                           23, 59, 59))
        axes[day_idx].grid()
        axes[day_idx].set_facecolor((0.9, 0.9, 0.9))

        if cgm_start_idx >= len(cgm_samples):
            # When there is no more data, show empty chart. We could break here,
            day_idx += 1  # but then remaining charts have different look
            logging.warning(f"There is no data for day {end_sample_time.date()} in the given "
                            "database.")
            end_sample_time += one_day
            continue  

        # print date and day in week at each plot
        axes[day_idx].text(dt.datetime(start_date.year, start_date.month, start_date.day, 0, 15, 0),
                           y_min + y_range / 30,  # 30 got experimentally
                           dt.datetime.strftime(cgm_samples[cgm_start_idx].timestamp,
                                                '%Y-%m-%d %a'))

        cgm_datetimes, cgm_values, _, cgm_start_idx = _get_samples_in_day(cgm_samples,
                                                                          start_date,
                                                                          cgm_start_idx,
                                                                          end_sample_time)
        list_to_selected_unit(cgm_values, gluco_unit)
        axes[day_idx].plot(cgm_datetimes, cgm_values)
        axes[day_idx].plot([cgm_datetimes[0], cgm_datetimes[-1]], [ref_min, ref_min], ':')
        axes[day_idx].plot([cgm_datetimes[0], cgm_datetimes[-1]], [ref_max, ref_max], ':')

        bg_test_datetimes, bg_test_values, _, bg_test_start_idx = \
                                                _get_samples_in_day(gmeter_samples,
                                                                    start_date,
                                                                    bg_test_start_idx,
                                                                    end_sample_time)
        list_to_selected_unit(bg_test_values, gluco_unit)
        axes[day_idx].plot(bg_test_datetimes, bg_test_values, 'gD')  # cyan diamond

        treat_datetimes, _, treat_desc, treat_start_idx = _get_samples_in_day(treatments_samples,
                                                                              start_date,
                                                                              treat_start_idx,
                                                                              end_sample_time)
        # values are not available for treatments, set them to define marker and text position
        y_pos_max = y_max - y_range / 6  # 1/6 of y range looks OK
        delta_y = y_range / 10  # 10 was obtained experimentally
        y_pos = y_pos_max
        note_values = []
        for x, desc in zip(treat_datetimes, treat_desc):
            # check if user entered BG value measured with finger prick
            try:
                val = float(desc)
                # this usually happens when values are given in other units than selected
                if val < y_min or val > y_max:
                    raise ValueError()  # show text the usual way in except below
            except ValueError:
                # change text Y position to avoid overlapping of text
                val = y_pos
                y_pos -= delta_y
                if y_pos < y_pos_max - 3 * delta_y:
                    y_pos = y_pos_max
            note_values.append(val)
            axes[day_idx].text(x, val, ' ' + desc, fontproperties=font_prop)

        axes[day_idx].plot(treat_datetimes, note_values, 'm*')

        _show_meals(meals, axes[day_idx], day_idx, start_date, y_min, y_max, font_prop)

        _plot_critical_values(axes[day_idx], cgm_datetimes, cgm_values, ref_min, ref_max)

        day_idx += 1
        end_sample_time += one_day

    axes[0].legend(['CGM', 
                    f'ref min({ref_min:.1f} {gluco_unit.value})',
                    f'ref max({ref_max:.1f} {gluco_unit.value})',
                    'finger prick tests', 'notes'],
                   loc=2)
    plt.ylabel(f'glucose [{gluco_unit.value}]')
    plt.xlabel('time in day [HH:MM]')
    # Fine-tune figure; make subplots close to each other and hide x ticks for
    # all but bottom plot.
    plt.subplots_adjust(left=0.06, right=0.98, top=0.98, bottom=0.04)
    plt.subplots_adjust(hspace=0.1)
    # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    if is_save_only:
        out_fname = dt.datetime.strftime(start_date, f"%Y-%m-%d_{no_of_days}-days.pdf")
        f.set_size_inches(10, 1.5 * no_of_days)
        f.savefig(out_fname)
        logging.info(f"Chart saved to file: {out_fname}")
    else:
        pyl.show()

    return


def _get_samples_in_day(bg_samples: List[BgSample], start_date: dt.datetime,
                        start_idx: int,
                        end_sample_time: dt.datetime) -> Tuple[List[dt.datetime],
                                                               List[float],
                                                               List[str],
                                                               int]:

    end_sample = BgSample(BgSources.BG_READINGS, end_sample_time, 0)
    end_idx = bisect.bisect_left(bg_samples, end_sample)

    datetimes: List[dt.datetime] = []
    values: List[float] = []
    descriptions = []
    for idx in range(start_idx, end_idx):
        ts = bg_samples[idx].timestamp
        # enable sharing of x-axis by overwriting date part of timestamp to the same value
        timestamp = dt.datetime(start_date.year, start_date.month, start_date.day,
                                ts.hour, ts.minute, ts.second)
        datetimes.append(timestamp)
        values.append(bg_samples[idx].bg_value_mmol_l)
        descriptions.append(bg_samples[idx].desc)

    start_idx = end_idx  # end_idx is not included in range above, it points to the first item
                         # on the following day (insertion point for bisect_left)

    return datetimes, values, descriptions, start_idx


def _plot_critical_values(axis, 
                          cgm_datetimes: List[dt.datetime], cgm_values: List[float],
                          ref_min, ref_max):
    critical_items = extract(cgm_datetimes, cgm_values, lambda x: x < ref_min)
    for critical_times, critical_values in critical_items:
        axis.plot(critical_times, critical_values, 'r')

    critical_items = extract(cgm_datetimes, cgm_values, lambda x: x > ref_max)
    for critical_times, critical_values in critical_items:
        axis.plot(critical_times, critical_values, color='orange')


def _show_meals(meals: List[MealData], axis, idx, start_date: dt.datetime,
                y_min: float, y_max: float, font_properties):
    year, month, day = start_date.year, start_date.month, start_date.day
    for meal in meals:

        hour, minute = meal.meal_time.hour, meal.meal_time.minute

        if idx == 0:  # show desc only in the topmost subplot
            y_pos = y_max - (y_max - y_min) / 12  # another experimental pos
            axis.text(dt.datetime(year, month, day, hour, minute, 0), y_pos, meal.description,
                      fontproperties=font_properties)

        x = dt.datetime(year, month, day, hour, minute, 0)
        axis.plot([x, x], [y_min, y_max], meal.line_style)
