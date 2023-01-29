#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from matplotlib import pyplot as plt


def basic_plot(x, y, title=None, xlabel=None, ylabel=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x, y)
    if title is not None:
        plt.suptitle(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.xlabel(ylabel)
    plt.show()


def basic_scatter(x, y=None, title=None, xlabel=None, ylabel=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if y is None:
        ax.scatter(x[:, 0], x[:, 1])
    else:
        ax.scatter(x, y)
    if title is not None:
        plt.suptitle(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.xlabel(ylabel)
    plt.show()
