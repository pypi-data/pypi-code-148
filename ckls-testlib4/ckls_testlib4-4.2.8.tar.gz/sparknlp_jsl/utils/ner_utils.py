from __future__ import division, print_function, unicode_literals
import numpy as np
from typing import Dict, List, Optional

from sparknlp_jsl.utils.imports import is_module_importable


def get_charts(log_file: str, threshold: float = 0.0):
    """
     Plots the figures of metrics ( precision, recall, f1) vs epochs

    :param log_file:  path to the log file

    """
    is_module_importable(lib='matplotlib',raise_exception=True,pip_name='matplotlib' )
    import matplotlib.pyplot as plt
    from sparknlp_jsl.utils.log_parse import __parse_logfile, __aggregate_entities
    metrics, avg_metrics, graph = __parse_logfile(log_file)
    chart_metrics = __aggregate_entities(metrics)
    avg_metrics = avg_metrics.replace({"Macro-average": "macro_avg", "Micro-average": "micro_avg"})

    fig, axs = plt.subplots(3, 2, figsize=(20, 20))
    fig.suptitle(graph)
    for j, s in enumerate(["validation", "test"]):
        try:
            for i, m in enumerate(["prec", "rec", "f1"]):
                avg_metrics[m] = avg_metrics[m].astype(np.float)
                cdf = avg_metrics[avg_metrics.set == s].reset_index()[["epoch", "metric", m]].pivot(index="epoch",
                                                                                                    columns="metric",
                                                                                                    values=m).reset_index().fillna(
                    0)
                axs[i][j].title.set_text(s + " - " + m)
                cdf.plot(x="epoch", ax=axs[i][j])
        except:
            pass

    fig, axs = plt.subplots(3, 2, figsize=(20, 20))
    fig.suptitle(graph)
    for j, s in enumerate(["validation", "test"]):
        try:
            for i, m in enumerate(["prec", "rec", "f1"]):
                cmr = chart_metrics.reset_index()
                cdf = cmr[(cmr.set == s) & (cmr.f1 > threshold)].reset_index()[["epoch", "entity", m]].pivot(
                    index="epoch", columns="entity", values=m).reset_index()
                axs[i][j].title.set_text(m)
                cdf.plot(x="epoch", ax=axs[i][j])
        except:
            pass


def loss_plot(log_path: str):
    """
     Plots the figure of loss vs epochs

    :param log_path: path to the log file
    """
    is_module_importable('matplotlib',True,'matplotlib' )
    import matplotlib.pyplot as plt

    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    loss = [line.split()[6] for line in lines if line.startswith("Epoch") and line.split()[6] != "size:"]

    epoch = []
    losses = []
    for x, y in enumerate(loss, 1):
        epoch.append(x)
        losses.append(float(y))

    plt.subplots(1, 1, figsize=(8, 8))
    plt.ylabel('Loss')
    plt.xlabel('Epochs')
    plt.title('Loss Plot')
    plt.plot(epoch[::-1], losses[::-1])
    plt.show()


def evaluate(true_seqs: List[str], pred_seqs: List[str], verbose=True):
    """
    if verbose, returns overall performance, as well as performance per chunk type;
    otherwise, simply returns overall precision, recall, f1 scores

    :param true_seqs: a list of true tags
    :param pred_seqs: a list of predicted tags
    :param verbose: boolean


    """
    from sparknlp_jsl.utils.conll_parse import __get_result, __count_chunks

    (correct_chunks, true_chunks, pred_chunks,
     correct_counts, true_counts, pred_counts) = __count_chunks(true_seqs, pred_seqs)
    result, chunk_metrics = __get_result(correct_chunks, true_chunks, pred_chunks,
                                         correct_counts, true_counts, pred_counts, verbose=verbose)
    return result, chunk_metrics


def evaluate_conll_file(fileIterator):
    """
     prints overall performance, as well as performance per chunk type
    """
    true_seqs, pred_seqs = [], []

    for line in fileIterator:
        cols = line.strip().split()
        # each non-empty line must contain >= 3 columns
        if not cols:
            true_seqs.append('O')
            pred_seqs.append('O')
        elif len(cols) < 3:
            raise IOError("conlleval: too few columns in line %s\n" % line)
        else:
            # extract tags from last 2 columns
            true_seqs.append(cols[-2])
            pred_seqs.append(cols[-1])
    return evaluate(true_seqs, pred_seqs)


