from __future__ import division, print_function, unicode_literals
import csv
import re

from sparknlp_jsl.utils.imports import is_module_importable

is_module_importable(lib='pandas',raise_exception=True,pip_name='pandas',message_type='module' )
import pandas as pd
from IPython.display import display


from typing import List

from .utils.training_log_parser_utils import aggregate_entities, count_chunks, get_result


class ner_log_parser:

    def __init__(self):

        """
        Class Constructor.
        """
        print("NER Log Parser Initiated")

    def parse_logfile(self, path: str):
        """
        Returns metrics and avg-metrics dataframes, graph name and a boolean for whether test set is provided or not.

        :param path: path to the log file

        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np

        logs = csv.reader(open(path, "r"), delimiter="\t")
        data = []
        avg_data = []
        test_set_defined = False
        for row in logs:
            if row and row[0].startswith("Name of the selected graph"):
                graph = row[0].split("/")[-1]
            if row and row[0].startswith("Epoch"):
                current_epoch = int(re.findall(r'\d+', row[0])[0])
            if row and row[0].startswith("Quality on"):
                set_idx = row[0].split(" ")[2]
            if row and row[0].startswith("Quality on test dataset"):
                test_set_defined = True
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
                graph, test_set_defined)

    def get_charts(self, log_file: str, threshold: float = 0.0):
        """
        Plots the figures of metrics ( precision, recall, f1) vs epochs

        :param log_file:  path to the log file

        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np
        is_module_importable('plotly',True,'plotly' )
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        metrics, avg_metrics, graph, test_flag = self.parse_logfile(log_file)
        chart_metrics = aggregate_entities(metrics)
        avg_metrics = avg_metrics.replace({"Macro-average": "macro_avg", "Micro-average": "micro_avg"})

        if test_flag:

            fig = make_subplots(rows=3, cols=2, subplot_titles=(
                "Validation Precision", "Test Precision", "Validation Recall", "Test Recall", "Validation F1",
                "Test F1",))

            for j, s in enumerate(["validation", "test"]):

                for i, m in enumerate(["prec", "rec", "f1"]):
                    avg_metrics[m] = avg_metrics[m].astype(np.float)
                    cdf = avg_metrics[avg_metrics.set == s].reset_index()[["epoch", "metric", m]].pivot(index="epoch",
                                                                                                        columns="metric",
                                                                                                        values=m).reset_index().fillna(
                        0)

                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["macro_avg"].values, mode="lines+markers",
                                   text=f"{m}-macro_avg", name=f"{m} macro_avg"),
                        row=i + 1, col=j + 1,
                    )
                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["micro_avg"].values, mode="lines+markers",
                                   text=f"{m}-micro_avg", name=f"{m}-micro_avg"),
                        row=i + 1, col=j + 1
                    )
            fig.update_layout(height=800, width=1200, title_text="Validation Scores vs Test Scores")
            fig.show()

        else:
            fig = make_subplots(rows=3, cols=1,
                                subplot_titles=("Validation Precision", "Validation Recall", "Validation F1"))

            for j, s in enumerate(["validation"]):

                for i, m in enumerate(["prec", "rec", "f1"]):
                    avg_metrics[m] = avg_metrics[m].astype(np.float)
                    cdf = avg_metrics[avg_metrics.set == s].reset_index()[["epoch", "metric", m]].pivot(index="epoch",
                                                                                                        columns="metric",
                                                                                                        values=m).reset_index().fillna(
                        0)

                    fig.add_trace(
                        # go.Scatter( x=cdf["epoch"], y=cdf["macro_avg"]),
                        go.Scatter(x=cdf["epoch"].index, y=cdf["macro_avg"].values, mode="lines+markers",
                                   text=f"{m}-macro_avg", name=f"{m} macro_avg"),
                        row=i + 1, col=j + 1,
                    )
                    fig.add_trace(
                        # go.Scatter( x=cdf["epoch"], y=cdf["macro_avg"]),
                        go.Scatter(x=cdf["epoch"].index, y=cdf["micro_avg"].values, mode="lines+markers",
                                   text=f"{m}-micro_avg", name=f"{m}-micro_avg"),
                        row=i + 1, col=j + 1
                    )
            fig.update_layout(height=800, width=1200, title_text="Validation Scores")
            fig.show()

    def loss_plot(self, log_path: str):
        """
        Plots the figure of loss vs epochs

        :param log_path: path to the log file
        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np
        is_module_importable('matplotlib',True,'matplotlib' )
        import matplotlib.pyplot as plt
        is_module_importable('plotly',True,'plotly' )
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            epoch = [int(line.split()[1].split("/")[0]) for line in lines if
                     line.startswith("Epoch") and "started" in line]
            validation_loss = [float(line.split()[3]) for line in lines if line.startswith("Total validation loss:")]

            if len(validation_loss) != 0:

                test_loss = [float(line.split()[3]) for line in lines if line.startswith("Total test loss:")]

                if len(test_loss) != 0:
                    df = pd.DataFrame(np.array([epoch, validation_loss, test_loss]).T,
                                      columns=["Epochs", "Validation Loss", "Test Loss"])

                    fig = make_subplots(rows=1, cols=2, subplot_titles=("Validation Loss", "Test Loss"))
                    fig.add_trace(
                        go.Scatter(x=df["Epochs"].index, y=df["Validation Loss"].values, mode="lines+markers",
                                   text="Validation Loss", name="Validation Loss"),
                        row=1, col=1,
                    )
                    fig.add_trace(
                        go.Scatter(x=df["Epochs"].index, y=df["Test Loss"].values, mode="lines+markers",
                                   text="Test Loss",
                                   name="Test Loss"),
                        row=1, col=2,
                    )
                    fig.update_layout(height=600, width=1200, title_text="Validation Scores vs Test Scores")
                    fig.show()

                else:
                    df = pd.DataFrame(np.array([epoch, validation_loss]).T,
                                      columns=["Epochs", "Validation Loss"])

                    fig = px.line(df, x="Epochs", y="Validation Loss", title=f'.. ')
                    fig.update_layout(title='Validation Loss Plot', )
                    fig.show()
            else:
                loss = [line.split()[6] for line in lines if line.startswith("Epoch") and line.split()[6] != "size:"]

                epoch = []
                losses = []
                for x, y in enumerate(loss, 1):
                    epoch.append(x)
                    losses.append(float(y))

                plt.subplots(1, 1, figsize=(8, 8))
                plt.ylabel('Loss')
                plt.xlabel('Epochs')
                plt.title('Validation Loss Plot')
                plt.plot(epoch[::-1], losses[::-1])
                plt.show()

    def get_best_f1_scores(self, log_path: str):
        """
        Returns the best Micro and Macro F1 Scores

        :param log_path: path to the log file
        """
        metrics, avg_metrics, graph, test_flag = self.parse_logfile(log_path)

        if test_flag:
            print("Best Micro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[
                avg_metrics[(avg_metrics.set == "test") & (avg_metrics.metric == "Micro-average")].f1.idxmax()].epoch])
            print("Best Macro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[
                avg_metrics[(avg_metrics.set == "test") & (avg_metrics.metric == "Macro-average")].f1.idxmax()].epoch])

        else:
            print("Best Micro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[avg_metrics[
                (avg_metrics.set == "validation") & (avg_metrics.metric == "Micro-average")].f1.idxmax()].epoch])
            print("Best Macro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[avg_metrics[
                (avg_metrics.set == "validation") & (avg_metrics.metric == "Macro-average")].f1.idxmax()].epoch])

    def evaluate(self, true_seqs: List[str], pred_seqs: List[str], verbose=True):
        """
        if verbose, returns overall performance, as well as performance per chunk type;
        otherwise, simply returns overall precision, recall, f1 scores
 
        :param true_seqs: a list of true tags
        :param pred_seqs: a list of predicted tags
        :param verbose: boolean
 
        """

        (correct_chunks, true_chunks, pred_chunks,
         correct_counts, true_counts, pred_counts) = count_chunks(true_seqs, pred_seqs)
        result, chunk_metrics = get_result(correct_chunks, true_chunks, pred_chunks,
                                           correct_counts, true_counts, pred_counts, verbose=verbose)
        return result, chunk_metrics

    def evaluate_conll_file(self, fileIterator):
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
        return self.evaluate(true_seqs, pred_seqs)


class assertion_log_parser:

    def __init__(self):

        """
        Class Constructor.
        """
        print("Assertion Log Parser Initiated")

    def parse_logfile(self, path: str, labels: List[str]):
        """
        Returns metrics and avg-metrics dataframes, graph name and a boolean for whether test set is provided or not.

        :param path: path to the log file
        :param labels: list of assertion labels
        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np

        logs = csv.reader(open(path, "r"), delimiter="\t")
        data = []
        avg_data = []
        test_set_defined = False
        for row in logs:
            if row and row[0].startswith("Name of the selected graph"):
                graph = row[0].split("/")[-1]
            if row and row[0].startswith("Epoch"):
                current_epoch = int(re.findall(r'\d+', row[0])[0])
            if row and row[0].startswith("Quality on"):
                set_idx = row[0].split(" ")[2]

            if row and row[0].startswith("Quality on test dataset"):
                test_set_defined = True
            if row and row[0] in labels:
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
                graph, test_set_defined)

    def get_charts(self, log_file: str, labels: List[str], threshold=0.0):
        """

        Plots the figures of metrics ( precision, recall, f1) vs epochs

        :param log_file:  path to the log file
        :param labels: list of assertion labels
        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np

        is_module_importable('plotly',True,'plotly' )
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        metrics, avg_metrics, graph, test_flag = self.parse_logfile(log_file, labels)
        chart_metrics = aggregate_entities(metrics)
        avg_metrics = avg_metrics.replace({"Macro-average": "macro_avg", "Micro-average": "micro_avg"})

        if test_flag:

            fig = make_subplots(rows=3, cols=2, subplot_titles=(
                "Validation Precision", "Test Precision", "Validation Recall", "Test Recall", "Validation F1",
                "Test F1",))

            for j, s in enumerate(["validation", "test"]):

                for i, m in enumerate(["prec", "rec", "f1"]):
                    avg_metrics[m] = avg_metrics[m].astype(np.float)
                    cdf = avg_metrics[avg_metrics.set == s].reset_index()[["epoch", "metric", m]].pivot(index="epoch",
                                                                                                        columns="metric",
                                                                                                        values=m).reset_index().fillna(
                        0)

                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["macro_avg"].values, mode="lines+markers",
                                   text=f"{m}-macro_avg", name=f"{m} macro_avg"),
                        row=i + 1, col=j + 1,
                    )
                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["micro_avg"].values, mode="lines+markers",
                                   text=f"{m}-micro_avg", name=f"{m}-micro_avg"),
                        row=i + 1, col=j + 1
                    )
            fig.update_layout(height=800, width=1200, title_text="Validation Scores vs Test Scores")
            fig.show()

        else:
            fig = make_subplots(rows=3, cols=1,
                                subplot_titles=("Validation Precision", "Validation Recall", "Validation F1"))

            for j, s in enumerate(["validation"]):

                for i, m in enumerate(["prec", "rec", "f1"]):
                    avg_metrics[m] = avg_metrics[m].astype(np.float)
                    cdf = avg_metrics[avg_metrics.set == s].reset_index()[["epoch", "metric", m]].pivot(index="epoch",
                                                                                                        columns="metric",
                                                                                                        values=m).reset_index().fillna(
                        0)

                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["macro_avg"].values, mode="lines+markers",
                                   text=f"{m}-macro_avg", name=f"{m} macro_avg"),
                        row=i + 1, col=j + 1,
                    )
                    fig.add_trace(
                        go.Scatter(x=cdf["epoch"].index, y=cdf["micro_avg"].values, mode="lines+markers",
                                   text=f"{m}-micro_avg", name=f"{m}-micro_avg"),
                        row=i + 1, col=j + 1
                    )
            fig.update_layout(height=800, width=1200, title_text="Validation Scores")
            fig.show()

    def loss_plot(self, log_path: str):

        """
        Plots the figure of loss vs epochs

        :param log_path: path to the log file
        """
        is_module_importable('numpy',True,'numpy' )
        import numpy as np

        is_module_importable('plotly',True,'plotly' )
        import plotly.express as px
        from plotly.subplots import make_subplots
        import plotly.graph_objects as go
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        epoch = [int(line.split()[1]) + 1 for line in lines if line.startswith("Epoch:")]
        validation_loss = [float(line.split()[3]) for line in lines if line.startswith("Total validation loss:")]
        test_loss = [float(line.split()[3]) for line in lines if line.startswith("Total test loss:")]

        if len(test_loss) != 0:
            df = pd.DataFrame(np.array([epoch, validation_loss, test_loss]).T,
                              columns=["Epochs", "Validation Loss", "Test Loss"])
            fig = make_subplots(rows=1, cols=2, subplot_titles=("Validation Loss", "Test Loss"))
            fig.add_trace(
                go.Scatter(x=df["Epochs"].index, y=df["Validation Loss"].values, mode="lines+markers",
                           text="Validation Loss", name="Validation Loss"),
                row=1, col=1,
            )
            fig.add_trace(
                go.Scatter(x=df["Epochs"].index, y=df["Test Loss"].values, mode="lines+markers", text="Test Loss",
                           name="Test Loss"),
                row=1, col=2,
            )
            fig.update_layout(height=600, width=1200, title_text="Validation Scores vs Test Scores")
            fig.show()

        else:
            df = pd.DataFrame(np.array([epoch, validation_loss]).T,
                              columns=["Epochs", "Validation Loss"])
            fig = px.line(df, x="Epochs", y="Validation Loss", title=f'.. ')
            fig.update_layout(title='Validation Loss Plot', )
            fig.show()

    def get_best_f1_scores(self, log_path: str, labels: List[str]):
        """
        Returns the best Micro and Macro F1 Scores

        :param log_path: path to the log file
        :param labels: list of assertion labels
        """
        metrics, avg_metrics, graph, test_flag = self.parse_logfile(log_path, labels)

        if test_flag:
            print("Best Micro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[
                avg_metrics[(avg_metrics.set == "test") & (avg_metrics.metric == "Micro-average")].f1.idxmax()].epoch])
            print("Best Macro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[
                avg_metrics[(avg_metrics.set == "test") & (avg_metrics.metric == "Macro-average")].f1.idxmax()].epoch])

        else:
            print("Best Micro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[avg_metrics[
                (avg_metrics.set == "validation") & (avg_metrics.metric == "Micro-average")].f1.idxmax()].epoch])
            print("Best Macro F1 Score :")
            display(avg_metrics[avg_metrics.epoch == avg_metrics.iloc[avg_metrics[
                (avg_metrics.set == "validation") & (avg_metrics.metric == "Macro-average")].f1.idxmax()].epoch])
