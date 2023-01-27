from functools import lru_cache
import os
from pathlib import Path
import time

from influx_line_protocol import Metric
import requests
#
# METRICS_LOG_DIR = Path(os.environ.get("METRICS_LOG", "/var/log/wf_metrics"))
#
# metlogger = logging.getLogger("wf_metrics")
# if not METRICS_LOG_DIR.exists():
#     METRICS_LOG_DIR.mkdir()
# path = METRICS_LOG_DIR / f"{os.environ.get('METRICS_NAME', 'control-uploader')}-{os.getpid()}.log"
# metlogger.setLevel(logging.INFO)
# handy = RotatingFileHandler(path, maxBytes=20000000, backupCount=5)
# handy.setFormatter(logging.Formatter())
# metlogger.addHandler(handy)
#
# def emit(name, values, tags=None):
#     metric = Metric(name)
#     metric.with_timestamp(time.time() * 1000000000)
#     if tags is None:
#         tags = {"tag": "team"}
#     for tag in tags:
#         metric.add_tag(tag, tags[tag])
#     for value in values:
#         metric.add_value(value, values[value])
#     metlogger.info(metric)
#
#
# @lru_cache(maxsize=2)
# def get_metrics_pipe():
#     METRICS_LOG_DIR = Path(os.environ.get("METRICS_LOG", "/var/log/wf_metrics"))
#     if not METRICS_LOG_DIR.exists():
#         METRICS_LOG_DIR.mkdir()
#     path = METRICS_LOG_DIR / f"{os.environ.get('METRICS_NAME', 'control-uploader')}"
#     if not path.exists():
#         os.mkfifo(path, 0o777)
#     return path
#
# def emit(name, values, tags=None):
#     path = get_metrics_pipe()
#     with open(path, 'w') as metrics_pipe:
#         metric = Metric(name)
#         metric.with_timestamp(time.time() * 1000000000)
#         if tags is None:
#             tags = {"tag": "team"}
#         for tag in tags:
#             metric.add_tag(tag, tags[tag])
#         for value in values:
#             metric.add_value(value, values[value])
#         metrics_pipe.write(str(metric))


def emit(name, values, tags=None):
    metric = Metric(name)
    metric.with_timestamp(time.time() * 1000000000)
    if tags is None:
        tags = {"tag": "team"}
    for tag in tags:
        metric.add_tag(tag, tags[tag])
    for value in values:
        metric.add_value(value, values[value])
    requests.post("http://localhost:8080/telegraf", data=str(metric).encode("utf8"))
