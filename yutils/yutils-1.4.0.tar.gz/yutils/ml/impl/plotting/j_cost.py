#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils._import import import_matplotlib
from yutils.ml.impl.plotting.base import get_model_name


def plot_j_cost(j_cost_history, model=None):
    plt = import_matplotlib()
    plt.plot(j_cost_history)
    if model:
        model_name = get_model_name(model)
        plt.suptitle(f'Hypothesis Cost by Iteration for {model_name}')
    plt.xlabel('Iteration')
    plt.ylabel('Cost (J)')
    plt.show()