import csv
import re
from sparknlp_jsl.utils.imports import is_module_importable


def __parse_logfile(path):
    is_module_importable('pandas',True,'pandas' )
    is_module_importable('numpy',True,'numpy' )
    import numpy as np
    import pandas as pd

    logs = csv.reader(open(path, "r"), delimiter="\t")
    data = []
    avg_data = []
    for row in logs:
        if row and row[0].startswith("Name of the selected graph"):
            graph = row[0].split("/")[-1]
        if row and row[0].startswith("Epoch"):
            current_epoch = int(re.findall(r'\d+', row[0])[0])
        if row and row[0].startswith("Quality on"):
            set_idx = row[0].split(" ")[2]
        if row and row[0][:2] in ["B-", "I-"]:
            data.append(
                (current_epoch, set_idx, row[0], row[0].split("-")[-1], *np.array(row[1:]).astype(np.float)))
        if row and row[0][:13] == "Macro-average":
            data_i = [d.split(": ")[-1] for d in row[1].split("\t")[-1].split(", ")]
            avg_data.append((current_epoch, set_idx, row[0], *np.array(data_i).astype(np.float)))
        if row and row[0][:13] == "Micro-average":
            data_i = [d.split(": ")[-1] for d in row[1].split("\t")[-1].split(", ")]
            avg_data.append((current_epoch, set_idx, row[0], *np.array(data_i).astype(np.float)))
    return (pd.DataFrame(data, columns=["epoch", "set", "label", "entity", "tp", "fp", "fn", "prec", "rec", "f1"]),
            pd.DataFrame(avg_data, columns=["epoch", "set", "metric", "prec", "rec", "f1"]),
            graph)


def __aggregate_entities(metrics):
    metrics["entity"] = metrics.label.apply(lambda x: x.split("-")[-1])
    chart_metrics = metrics[["epoch", "set", "entity", "tp", "fp", "fn"]].groupby(["epoch", "entity", "set"]).sum()
    chart_metrics["prec"] = chart_metrics.tp / (chart_metrics.tp + chart_metrics.fp)
    chart_metrics["rec"] = chart_metrics.tp / (chart_metrics.tp + chart_metrics.fn)
    chart_metrics["f1"] = 2 * chart_metrics.prec * chart_metrics.rec / (chart_metrics.prec + chart_metrics.rec)
    return chart_metrics