import argparse
import datetime

from py_kaos_utils.argparse import ArgParseTypes


def test_ArgParseTypes_datetime():
    parser = argparse.ArgumentParser()
    parser.add_argument('datetime', type=ArgParseTypes.datetime)

    args = parser.parse_args(["Aug 25th 2022"])
    # or vars(args)['datetime']
    assert args.datetime == datetime.datetime(2022, 8, 25)
