import sys
from fifeutil.timing import TimerSyncHour
import datetime
import argparse
import numpy as np
import json
import time
import logging

log = logging.getLogger(__name__)


def report_measurement():
    dt = datetime.datetime.now()
    sin_day = np.sin(((dt.hour * 60 + dt.minute) * 60 + dt.second) / 60.0 / 60.0 / 24.0 * 2 * np.pi)
    cos_day = np.sin(((dt.hour * 60 + dt.minute) * 60 + dt.second) / 60.0 / 60.0 / 24.0 * 2 * np.pi)
    field1 = 13.0 - sin_day * 2.0 + np.random.normal(0.0, 0.05)
    field2 = cos_day + np.random.normal(0.0, 0.05)
    data = {"ts": time.time(), "V": field1, "I": field2, "P": field1 * field2}
    print(json.dumps(data))
    sys.stdout.flush()  # important - otherwise when piping, Python may buffer this output for some reason


def main():
    parser = argparse.ArgumentParser(description=(
        'Fake INA226 device - reports status at regular intervals'))
    parser.add_argument('--sph', default=60 * 12, help='samples per hour (default=False)',
                        type=float)
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default='INFO')
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel.upper())
    log.info("Fake INA226 device")
    measurementtimer = TimerSyncHour(args.sph)
    measurementtimer.triggercallback(report_measurement)


if __name__ == '__main__':
    main()
