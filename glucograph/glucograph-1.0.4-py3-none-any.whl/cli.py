#!/usr/env python
import logging
import argparse
import sqlite3
import datetime as dt
import glucograph.analyzer as bga
import glucograph.diagram as diagram


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This script shows data from Dexcom sensor "
                                                 "in charts.",
                                     epilog="""
Examples:

  Shows diagrams starting at 2022-09-10 for next 7 days:
  
      glucograph --gmeter data/next_one-2023-01-09.csv data/next-link-2023-01-09.csv --start 2022-09-10 --days 7 ../data/export20230102-205553.sqlite

  Prints statistics:
  
      glucograph --stats ../data/export20230102-205553.sqlite
""")

    parser.add_argument("-l", "--loglevel", dest='log_level',
                        choices=['d', 'i', 'w', 'e'],
                        default='i',
                        help="log level, one of d, i, w, e", type=str)

    sdate = dt.datetime.now() - dt.timedelta(days=7)
    parser.add_argument("-s", "--start", default=sdate.strftime("%Y-%m-%d"),
                        help="start date time in ISO format: yyyy-mm-dd", type=str)

    parser.add_argument("-d", "--days", dest='no_of_days',
                        help="number of days to show in the chart", type=int, default=7)

    parser.add_argument("--ymin", dest='y_min',
                        help="min value on y axis in selected unit.", type=float, default=-1)

    parser.add_argument("--ymax", dest='y_max',
                        help="max value on y axis in selected unit", type=float, default=-1)

    parser.add_argument("--ref_min", dest='ref_min', type=float, default=-1,
                        help="reference for low blood glucose level in selected unit")

    parser.add_argument("--ref_max", dest='ref_max', type=float, default=-1,
                        help="reference for high blood glucose level in selected unit")

    parser.add_argument("--stats", dest='is_print_statistics',
                        help="displays overview of data in the file, such as start "
                             "date, end date, ... No chart is drawn if this option is specified. "
                             "Options for start date and no of days are ignored.",
                        action='store_true')

    parser.add_argument("--gmeter", dest='gmeter_csv_fname', nargs='*', default=[],
                        help='names of files with data from glucose meter (for '
                                         'example Contour Next One) in csv format: '
                                         "'2020-08-09 12:23:51, 3.7, mmol/L'")

    parser.add_argument("--meals", dest='meals_csv_fname', type=str, default=[],
                        help='name of file with meals. Use this options for meals or other '
                             'intake regular on a daily basis. File should contain meal time, '
                             'line style in matplotlib format, and description, for example: '
                             '9:30, r-, CS 30g')

    parser.add_argument("--mgdl", dest='is_mgdl_gluco_unit', action='store_true',
                        default=False,
                        help='If specified, mg/dl are used as glucose units. Default are mmol/l')

    parser.add_argument("--show_treatments", dest='is_show_treatments', action='store_true',
                        default=False,
                        help='If specified, treatments entered into xDrip are shown in charts.')

    parser.add_argument("--show_calibrations", dest='is_show_calibrations', action='store_true',
                        default=False,
                        help='If specified, calibrations (finger prick measurements) entered '
                             'into xDrip are shown in charts.')

    parser.add_argument("--save", dest='is_save_only', action='store_true', default=False,
                        help='If specified, image is save to file instead of shown on screen.')

    parser.add_argument("file_name", help='Name of sqlite file exported from xDrip '
                                          'with option ... | Imxport / Export Features '
                                          '| Export database')
    args = parser.parse_args()
    return args


def main():
    log_map = {'d': logging.DEBUG, 'i': logging.INFO, 'w': logging.WARNING, 'e': logging.ERROR}

    options = parse_args()
    logging.basicConfig(level=log_map[options.log_level])
    cgm_db = sqlite3.connect(options.file_name)

    gluco_unit = bga.GlucoseUnits.MG_DL if options.is_mgdl_gluco_unit else bga.GlucoseUnits.MMOL_L

    # Use defaults if user did not specify value in cmd line. Defaults can not
    # be specified in arg parser, because they depend on selected BG unit.
    y_min = options.y_min if options.y_min >= 0 else bga.to_selected_unit(3, gluco_unit)
    y_max = options.y_ax if options.y_max >= 0 else bga.to_selected_unit(9, gluco_unit)
    ref_min = options.ref_min if options.ref_min >= 0 else bga.to_selected_unit(4.2, gluco_unit)
    # see https://en.wikipedia.org/wiki/Blood_sugar_level
    ref_max = options.ref_max if options.ref_max >= 0 else bga.to_selected_unit(10, gluco_unit)

    try:
        cgm_samples = bga.read_table_bg_readings(cgm_db)
        treatments_samples = bga.read_table_treatments(cgm_db)
        blood_test_samples = bga.read_table_blood_test(cgm_db)

        # merge data from glucometers and xDrip, since not all glucometers
        # support reading of stored data, so xDrip may contain more data.
        gmeter_samples = bga.read_glucometer_files(options.gmeter_csv_fname)
        gmeter_samples.extend(blood_test_samples)
        gmeter_samples.sort()

        meals = bga.read_meals(options.meals_csv_fname) if options.meals_csv_fname else []

        if options.start:
            start_date: dt.datetime = dt.datetime.fromisoformat(options.start)
        else:
            start_date = blood_test_samples[0].timestamp

        if options.is_print_statistics:
            bga.print_stats(cgm_samples)
            diffs, avg_diff_as_func_of_meter_val = bga.analyze_meter_cgm_diff(gmeter_samples,
                                                                              cgm_samples)
            print(diffs, avg_diff_as_func_of_meter_val)
        else:
            diagram.plot_cgm_data(cgm_samples, gmeter_samples, treatments_samples,
                                  gluco_unit,
                                  meals,
                                  start_date, options.no_of_days,
                                  y_min,
                                  y_max,
                                  options.is_save_only,
                                  ref_min,
                                  ref_max)

    except Exception as ex:
        logging.error(f"ERROR: {ex}", exc_info=ex)


if __name__ == '__main__':
    main()
